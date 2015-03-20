
import os
import pdb
import time
import traceback
import gaiatest

from optparse import OptionParser
from marionette import Marionette
from marionette.by import By
from marionette.wait import Wait


class InstallAppError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class installApp():
    
    _confirm_install_button_locator = (By.ID, 'app-install-install-button')
    _confirm_allow_button_locator = (By.ID, 'app-install-install-button')
    _homescreen_all_icons_locator = (By.CSS_SELECTOR, 'gaia-grid .icon:not(.placeholder)')

    def __init__(self):
        self.marionette = Marionette(host='localhost', port=int('2828'))
        self.marionette.start_session()

    def install(self,app_name):
        #get gaia_app.js absolute path 
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, "gaia_apps.js"))
        self.marionette.import_script(js)

        if not self.is_app_installed(app_name):
            url = 'https://firefox:blackswan@'+ app_name + '.fx-webapps.com'+'/manifest.webapp'
            print "install app: "+app_name+", url is: "+url
            # Install app
            try:
                self.marionette.execute_script(
                    'navigator.mozApps.install("%s")' % url)

                # Confirm the installation and wait for the app icon to be present
                self.tap_confirm() 
                self.switch_to_displayed_app()
                self.check_installed_app(app_name)
            except :
                traceback.print_exc()
        else:
            print app_name +" is already installed"

    def is_app_installed(self, app_name):
        self.marionette.switch_to_frame()
        return self.marionette.execute_async_script("GaiaApps.locateWithName('%s')" % app_name)

    def tap_confirm(self):
        self.wait_for_element_displayed(*self._confirm_install_button_locator)
        self.marionette.find_element(*self._confirm_install_button_locator).tap()

    def switch_to_displayed_app(self):
        self.marionette.switch_to_default_content()

        self.marionette.switch_to_frame()
        result = self.marionette.execute_script('return GaiaApps.getDisplayedApp();')
        self.marionette.switch_to_frame(result.get('frame'))    

    def wait_for_element_displayed(self, by, locator, timeout=20):
        Wait(self.marionette, timeout).until(
            lambda m: m.find_element(by, locator).is_displayed())

    def check_installed_app(self, app_name):        
        isFound = False

        for root_el in self.marionette.find_elements(*self._homescreen_all_icons_locator):
            if root_el.text == app_name.capitalize():
                isFound = True

        if not isFound:
            print app_name +" is not found, install failed"

    def get_app_name(self):        
        parser = dzOptionParser(usage='%prog [options] filename')
        parser.add_option('--filename',
                      action='store',
                      dest='filename',
                      default=None,
                      type='str',
                      help='path to a app list file with any test data required')
        parser.add_option('--testvars',
                      action='store',
                      dest='testvars',
                      metavar='str',
                      help='path to a json file with any test data required')

        options, args = parser.parse_args()        

        if options.filename:
            if not os.path.exists(options.filename):
                raise InstallAppError('--filename file does not exist')

        self.testvars = {}
        if options.testvars:
            if not os.path.exists(options.testvars):
                raise InstallAppError('--testvars file does not exist')

            import json
            with open(options.testvars) as f:
                self.testvars = json.loads(f.read())

        app_name = []

        fp = file(options.filename)

        for (linenum, line) in enumerate(fp.readlines(), start=1):

            stripped = line.strip()

            # ignore blank lines
            if not stripped:
                # reset key and value to avoid continuation lines
                key = value = None
                continue
            
            # ignore comment lines
            if stripped[0] in ';#':
                continue

            app_name.append(stripped)

        return app_name

    def connect_to_network(self):
        self.data_layer = gaiatest.GaiaData(self.marionette,self.testvars)

        if  self.data_layer.is_wifi_connected() == False:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi()

class dzOptionParser(OptionParser):
    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)

if __name__ == '__main__':
    app_install = installApp()

    app_name = app_install.get_app_name()
    app_install.connect_to_network()

    for i in range (len(app_name)):
        app_install.install(app_name[i])
    app_install.marionette.delete_session()
