
import time
from marionette.by import By
from app_common import AppCommon

class Camera(AppCommon):
    name = "SOMC Camera"

    video = (By.CSS_SELECTOR, 'body')
    settingsButton = (By.CSS_SELECTOR, 'span.sfi-cam-options')
    settingsSubMenu = (By.CSS_SELECTOR, 'div.modal-dialog.modal-option')
    settingsSubMenuTabCamera = (By.CSS_SELECTOR, 'span.sfi-cam-camera')
    settingsSubMenuTabVideo = (By.CSS_SELECTOR, 'span.sfi-cam-video')
    settingsSubMenuTabOther = (By.CSS_SELECTOR, 'span.sfi-cam-settings')
    CameraSubMenuTabBody = (By.CSS_SELECTOR, 'div#setting_pane_photo.tab-pane.active')
    VideoSubMenuTabBody = (By.CSS_SELECTOR, 'div#setting_pane_video.tab-pane.active')
    OtherSubMenuTabBody = (By.CSS_SELECTOR, 'div#setting_pane_other.tab-pane.active')
    flashModeButton = (By.CSS_SELECTOR, 'span.sfi-cam-flash-auto')
    flashModeSubMenu = (By.CSS_SELECTOR, 'span.list-icon.sfi-cam-flash-auto')
    capturePhotoButton = (By.CSS_SELECTOR, 'div#captureButton.icon-capture-photo')
    captureVideoButtonOFF = (By.CSS_SELECTOR, 'div.icon-capture-video')
    captureVideoButtonON = (By.CSS_SELECTOR, 'div.icon-capture-video-rec-pressed')
    lastSnapshotWrapperPhoto = (By.CSS_SELECTOR, 'div.last-snapshot-wrapper')


    def setting_menu_displayed(self):
        if self.is_element_displayed(*self.video):
            if self.is_element_displayed(*self.settingsButton):
                self.marionette.find_element(*self.settingsButton).tap()
                self.wait_for_element_displayed(*self.settingsSubMenu)
                return self.is_element_displayed(*self.settingsSubMenu)
            else:
                return 'the settings Button is not found'
        else:
            return 'the camera app cannot find the locator : video'

    def setting_menu_tab_camera_displayed(self):
        if self.is_element_displayed(*self.settingsSubMenuTabCamera):
            self.marionette.find_element(*self.settingsSubMenuTabCamera).tap()
            self.wait_for_element_displayed(*self.CameraSubMenuTabBody)
            return self.is_element_displayed(*self.CameraSubMenuTabBody)
        else:
            return 'the settings submenu camera tab is not found'

    def setting_menu_tab_video_displayed(self):
        if self.is_element_displayed(*self.settingsSubMenuTabVideo):
            self.marionette.find_element(*self.settingsSubMenuTabVideo).tap()
            self.wait_for_element_displayed(*self.VideoSubMenuTabBody)
            return self.is_element_displayed(*self.VideoSubMenuTabBody)
        else:
            return 'the settings submenu video tab is not found'

    def setting_menu_tab_other_displayed(self):
        if self.is_element_displayed(*self.settingsSubMenuTabOther):
            self.marionette.find_element(*self.settingsSubMenuTabOther).tap()
            self.wait_for_element_displayed(*self.OtherSubMenuTabBody)
            return self.is_element_displayed(*self.OtherSubMenuTabBody)
        else:
            return 'the settings submenu other tab is not found'

    def flash_mode_displayed(self):
        if self.is_element_displayed(*self.flashModeButton):
            self.marionette.find_element(*self.flashModeButton).tap()
            self.wait_for_element_displayed(*self.flashModeSubMenu)
            self.marionette.find_element(*self.flashModeSubMenu).tap()
            self.wait_for_element_displayed(*self.video)
            return self.is_element_displayed(*self.video)
        else:
            return 'the flash mode button is not found'


    def capture_photo_button_works(self):
        if self.is_element_displayed(*self.capturePhotoButton):
            self.marionette.find_element(*self.capturePhotoButton).tap()
            self.wait_for_element_displayed(*self.lastSnapshotWrapperPhoto)
            if self.is_element_displayed(*self.lastSnapshotWrapperPhoto):
                return 'the last snapshot wrapper photo is found'
            else:
                return 'the last snapshot wrapper photo is not found'
        else:
            return 'capture photo Button is not found'

    def capture_video_button_works(self):
        if self.is_element_displayed(*self.captureVideoButtonOFF):
            self.marionette.find_element(*self.captureVideoButtonOFF).tap()
            self.wait_for_element_displayed(*self.captureVideoButtonON)
            if self.is_element_displayed(*self.captureVideoButtonON):
                time.sleep(3)
                self.marionette.find_element(*self.captureVideoButtonON).tap()
                self.wait_for_element_displayed(*self.lastSnapshotWrapperPhoto)
                if self.is_element_displayed(*self.lastSnapshotWrapperPhoto):
                    return 'the last snapshot wrapper photo is found'
                else:
                    return 'the last snapshot wrapper photo is not found'
            else:
                return 'capture video button is not enabled and the video is not recoding'
        else:
            return 'capture video Button is not found'
