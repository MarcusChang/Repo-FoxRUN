
import time

from mtbf_driver.mtbf_apps.ui_tests.app import UiTests
from mtbf_driver.mtbf_apps.ui_tests.app import MTBF_UiTests
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from webapptest.base.album import Album

class TestMtbfAlbum(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_network()
        self.ui_tests = UiTests(self.marionette)
        self.mtbf_ui_tests = MTBF_UiTests(self.marionette)
        self.mtbf_ui_tests.back_to_main_screen()
        self.app = Album(self.marionette)
        self.app.setUp()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.item)

    def test_album_single_picture_view(self):
        self.assertTrue(self.app.main_to_single(), 'full screen image should be displayed')
        self.assertTrue(self.app.single_tap_show_back(), 'back button should be displayed')
        result = self.app.single_flick()
        self.assertNotEqual(result[0], result[1], "swipe to next image")
        self.assertTrue(self.app.single_to_main(), 'the list is not empty')
