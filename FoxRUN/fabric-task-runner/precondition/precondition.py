
import os
import time
import traceback
import gaiatest
import pdb

from optparse import OptionParser
from marionette import Marionette
from marionette.by import By
from marionette.wait import Wait

class Precondiction_Setting():
    _confirm_next_button_locator = (By.ID, 'forward')
    _confirm_skip_button_locator = (By.ID, 'skip-tutorial-button')
    wait_short=1
    wait_middle=5
    adb = "adb "
    adbs= adb +"-s "

    def setting(self):
        self.marionette = Marionette(host='localhost', port=int('2828'))
        self.marionette.start_session()
        self.data_layer = gaiatest.GaiaData(self.marionette)

        result = self.data_layer.get_setting("screen.timeout")
        if result != 0:
            #disable ftu
            js = os.path.join(os.path.realpath(os.path.dirname(__file__)), "async_storage.js")
            self.marionette.import_script(js)
            self.marionette.execute_script("asyncStorage.setItem('ftu.enabled',false)")

            #setting
            self.data_layer.set_setting("screen.timeout",0)
            self.data_layer.set_setting("language.current","en-US")
            self.data_layer.set_setting("keyboard.current","en")
            self.data_layer.set_setting("lockscreen.enabled",False)
            self.data_layer.set_setting("lockscreen.locked",False)
            self.data_layer.set_setting("debugger.remote-mode","adb-devtools")

    def reboot(self, device):
        self.marionette.delete_session()

        reboot=" reboot"

        if (device == 'none'):
             shellcommand=self.adb + reboot + "; timeout 120 " + self.adb + " wait-for-device"
        else:
            shellcommand=self.adbs + device + reboot + "; timeout 120 " + self.adbs + device + " wait-for-device"
        print shellcommand
        os.system(shellcommand)

    def get_device_serial(self):
        parser = dzOptionParser(usage='%prog [options] device-serial')
        parser.add_option('--device-serial',
                      action='store',
                      dest='device_serial',
                      metavar='str',
                      help='serial identifier of device to target')

        options, args = parser.parse_args()
        return options.device_serial

class dzOptionParser(OptionParser):
    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)

if __name__ == '__main__':
    forward = " forward tcp:2828 tcp:2828"

    pre = Precondiction_Setting()
    device=pre.get_device_serial()

    if (device == 'none'):
        shellcommand=pre.adb + forward
    else:
        shellcommand=pre.adbs + device + forward

    os.system(shellcommand)
    pre.setting()
    pre.reboot(device)
