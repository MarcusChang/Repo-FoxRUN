
import time
from gaiatest import GaiaEnduranceTestCase
from webapptest.base.walkman import Walkman

class TestEnduranceWalkman(GaiaEnduranceTestCase):
    def setUp(self):
        GaiaEnduranceTestCase.setUp(self)
        self.connect_to_network()
        self.app = Walkman(self.marionette)
        self.app.setUp()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.item)

    def test_walkman_load_start_page(self):
        self.drive(test=self.load_start_page,  app='Walkman')

    def test_walkman_play_music(self):
        self.drive(test=self.play_music,  app='Walkman')

    def test_walkman_navigate_by_drawer(self):
        self.drive(test=self.navigate_by_drawer,  app='Walkman')

    def load_start_page(self):
        self.assertTrue(self.app.is_elements_displayed(*self.app.item), 'the list is not empty')
        result = self.app.scroll_mainview()
        self.assertEqual(result[0], result[1], "top transparent bar should be fixed when scroll")

    def play_music(self):
        self.assertTrue(self.app.show_drawer(),'drawer should be shown')
        self.assertTrue(self.app.show_tracklist(), 'the track list is not empty')
        self.assertTrue(self.app.press_tracklist(), 'mini player should in play state')
        time.sleep(2)
        self.assertTrue(self.app.press_pause(), 'mini player should in pause state')
        self.assertTrue(self.app.show_drawer(),'drawer should be shown again')
        self.assertTrue(self.app.show_mainview(),'first item should be shown')

    def navigate_by_drawer(self):
        self.assertTrue(self.app.show_drawer(),'drawer should be shown')
        self.assertTrue(self.app.show_playlist(),'playlist view should be shown')
        self.assertTrue(self.app.show_drawer(),'drawer should be shown again')
        self.assertTrue(self.app.show_mainview(),'first item should be shown')
