import os
import time
import gaiatest
import mozdevice
from marionette.by import By
from marionette.wait import Wait
from marionette.marionette import Actions
from gaiatest.apps.base import Base


class AppCommon(Base):

    confirm_install_button_locator = (By.ID, 'permission-yes')
    wait_long=10
    wait_short=2
    sdcard_path="/sdcard/tests/"

    def is_element_displayed(self,  method, target):
        return self.marionette.find_element(method, target).is_displayed()

    def is_elements_displayed(self,  method, target):
        list = self.marionette.find_elements(method, target)
        if (len(list) <=0):
            return false
        return list[0].is_displayed()

    def tap_confirm(self):
        time.sleep(self.wait_long)
        self.marionette.switch_to_frame()
        if (self.is_element_displayed(*self.confirm_install_button_locator)):
            self.wait_for_element_displayed(*self.confirm_install_button_locator)
            self.marionette.find_element(*self.confirm_install_button_locator).tap()
        self.marionette.switch_to_frame(self.app.frame_id)

    def _flick(self, direction,app_name):
        """Flick current monthly calendar to next or previous month.
        @param direction: flick to next month if direction='next', else flick to previous month
        """
        action = Actions(self.marionette)
        element = self.marionette.find_element(*self.body)

        if app_name  == 'Walkman':
            x_start = element.size['width'] / 4
            x_end = element.size['width'] / 4
            y_start = (element.size['height'] / 100) * (direction == 'next' and 90 or 10)
            y_end = (element.size['height'] / 100) * (direction == 'next' and 10 or 90)
        elif app_name  == 'Album':
            x_start = (element.size['width'] / 100) * (direction == 'next' and 90 or 10)
            x_end = (element.size['width'] / 100) * (direction == 'next' and 10 or 90)
            y_start = element.size['height'] / 4
            y_end = element.size['height'] / 4

        action.flick(element, x_start, y_start, x_end, y_end, 200).perform()
        time.sleep(self.wait_short)

    def push_media(self,app_name,device_serial):
        path = self.get_filepath(app_name)

        dm = mozdevice.DeviceManagerADB(deviceSerial=device_serial)
        self.device = gaiatest.GaiaDevice(self.marionette, manager=dm)

        if self.device.file_manager.dir_exists(self.sdcard_path+app_name) == False:
            self.device.file_manager.push_file(path)

    def get_filepath(self, filename):
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))

        return os.path.abspath(os.path.join(path, 'test_media', filename))
