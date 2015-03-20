
import time
from marionette.by import By
from app_common import AppCommon

class Album(AppCommon):
    name = "Album"

    body = (By.CSS_SELECTOR, 'body')
    item = (By.CSS_SELECTOR, 'span.swac-grid-item-content')
    menuButton = (By.CSS_SELECTOR, '#header .swac-actions')
    menuOverlay = (By.CSS_SELECTOR, '#menu')
    navButton = (By.CSS_SELECTOR, 'a.swac-action-nav')
    drawer = (By.CSS_SELECTOR, '.swac-drawer')
    drawerItem = (By.CSS_SELECTOR, '.swac-drawer ul li a')
    singleViewImage = (By.CSS_SELECTOR, 'div.fullscreen')
    singleViewImageNext = (By.CSS_SELECTOR, '.fullscreen .nextItem')
    singleViewBack = (By.CSS_SELECTOR, 'a.swac-action-nav')

    def setUp(self):
        self.push_media(self.name,self.marionette.device_serial)

    def main_to_single(self):
        itemToOpen = 1
        self.marionette.find_elements(*self.item)[itemToOpen].tap()
        self.wait_for_element_displayed(*self.singleViewImage)
        return self.is_element_displayed(*self.singleViewImage)

    def single_tap_show_back(self):
        self.marionette.find_element(*self.singleViewImage).tap()
        self.wait_for_element_displayed(*self.singleViewBack)
        return self.is_element_displayed(*self.singleViewBack)

    def single_flick(self):
        currentImage1 = self.marionette.find_element(*self.singleViewImage)
        self._flick("next",self.name)
        self.wait_for_element_displayed(*self.singleViewImage)
        currentImage2 = self.marionette.find_element(*self.singleViewImage)
        return (currentImage1, currentImage2)

    def single_to_main(self):
        self.marionette.find_element(*self.singleViewBack).tap()

        self.wait_for_element_displayed(*self.item)
        return self.is_elements_displayed(*self.item)

