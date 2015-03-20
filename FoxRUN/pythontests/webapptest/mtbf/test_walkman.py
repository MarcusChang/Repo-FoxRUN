
import time

from mtbf_driver.mtbf_apps.ui_tests.app import UiTests
from mtbf_driver.mtbf_apps.ui_tests.app import MTBF_UiTests
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from webapptest.base.walkman import Walkman

class TestMtbfWalkman(GaiaMtbfTestCase):
    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_network()

        #self.app_id = self.launch_by_touch("Walkman")
        self.ui_tests = UiTests(self.marionette)
        self.mtbf_ui_tests = MTBF_UiTests(self.marionette)
        self.mtbf_ui_tests.back_to_main_screen()
        self.app = Walkman(self.marionette)
        self.app.setUp()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.item)

    def test_walkman_play_music(self):
        self.assertTrue(self.app.show_drawer(),'drawer should be shown')
        self.assertTrue(self.app.show_tracklist(), 'the track list is not empty')
        self.assertTrue(self.app.press_tracklist(), 'mini player should in play state')
        time.sleep(2)
        self.assertTrue(self.app.press_pause(), 'mini player should in pause state')
        self.assertTrue(self.app.show_drawer(),'drawer should be shown again')
        self.assertTrue(self.app.show_mainview(),'first item should be shown')
