
import time
from marionette.by import By
from app_common import AppCommon

class Movies(AppCommon):
    name = "Movies"
    start = "00:00"

    item = (By.CSS_SELECTOR, 'span.swac-grid-item-content')
    menuButton = (By.CSS_SELECTOR, 'div.swac-top-bar div.swac-actions button.open-menu')
    menuPinchIn = (By.CSS_SELECTOR, 'div.swac-actions .swac-top-menu-container ul.swac-top-menu li:nth-child(2) a')
    menuPinchOut = (By.CSS_SELECTOR, 'div.swac-actions .swac-top-menu-container ul.swac-top-menu li:nth-child(3) a')
    videoPreview = (By.CSS_SELECTOR, 'video#video-preview')
    singleViewPlayer = (By.CSS_SELECTOR, 'div#player.ng-scope')
    singleViewProgress = (By.CSS_SELECTOR, 'div#player div.control-area')
    singleViewProgressText = (By.CSS_SELECTOR, 'span.time-display.ng-binding')
    singleViewBack = (By.CSS_SELECTOR, 'div.swac-top-bar span.swac-action-nav')

    def setUp(self):
        self.push_media(self.name,self.marionette.device_serial)

    def main_pinch(self, inout):
        itemToCompare = 1
        size1 = self.marionette.find_elements(*self.item)[itemToCompare].size["width"]
        self.marionette.find_element(*self.menuButton).click()
        if inout == 'out':
            self.wait_for_element_displayed(*self.menuPinchOut)
            self.marionette.find_element(*self.menuPinchOut).click()
        else:
            self.wait_for_element_displayed(*self.menuPinchIn)
            self.marionette.find_element(*self.menuPinchIn).click()
        self.wait_for_element_displayed(*self.item)
        size2 = self.marionette.find_elements(*self.item)[itemToCompare].size["width"]
        time.sleep(1)
        return (size1,  size2)

    def play_movie(self):
        itemToOpen = 2
        self.marionette.find_elements(*self.item)[itemToOpen].click()
        self.wait_for_element_displayed(*self.singleViewPlayer)
        return self.is_element_displayed(*self.singleViewPlayer)

    def get_player_progress(self):
        text = self.marionette.find_element(*self.singleViewProgressText).text
        length = len(self.start)
        current = text[:length]
        return current

    def player_to_main(self):
        self.marionette.find_element(*self.singleViewPlayer).tap()
        self.wait_for_element_displayed(*self.singleViewBack)
        self.marionette.find_element(*self.singleViewBack).click()
        self.wait_for_element_displayed(*self.videoPreview)
        return self.is_element_displayed(*self.videoPreview)

    def init_home(self, circle):
        for i in range(0, circle):
            self.main_pinch("out")
