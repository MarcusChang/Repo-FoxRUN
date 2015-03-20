
import time

from mtbf_driver.mtbf_apps.ui_tests.app import UiTests
from mtbf_driver.mtbf_apps.ui_tests.app import MTBF_UiTests
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from webapptest.base.movies import Movies

class TestUiMovies(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_network()
        self.app = Movies(self.marionette)
        self.app.setUp()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.item)

    def test_movies_startup(self):
        #init the home page grid item size to the largest.
        self.app.init_home(3)
        # test begin
        result = self.app.main_pinch("in")
        self.assertNotEqual(result[0], result[1], "item width should not same after pinch in 1")
        result = self.app.main_pinch("in")
        self.assertNotEqual(result[0], result[1], "item width should not same after pinch in 2")
        result = self.app.main_pinch("in")
        self.assertNotEqual(result[0], result[1], "item width should not same after pinch in 3")
        result = self.app.main_pinch("out")
        self.assertNotEqual(result[0], result[1], "item width should not same after pinch out 1")
        result = self.app.main_pinch("out")
        self.assertNotEqual(result[0], result[1], "item width should not same after pinch out 2")
        result = self.app.main_pinch("out")
        self.assertNotEqual(result[0], result[1], "item width should not same after pinch out 3")

    def test_movies_play_a_movie(self):
        self.assertTrue(self.app.play_movie(),'full screen video should be displayed')
        self.assertTrue(self.app.is_element_displayed(*self.app.singleViewProgress),'video progress should be displayed')
        time.sleep(2)
        current = self.app.get_player_progress()
        self.assertTrue(current > self.app.start,'video should be playing')
        time.sleep(3)
        self.assertFalse(self.app.is_element_displayed(*self.app.singleViewProgressText),'video progress should not be displayed')
        self.assertTrue(self.app.player_to_main(),'video preview should be displayed')
