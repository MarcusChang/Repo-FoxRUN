
from gaiatest import GaiaTestCase
from webapptest.mixins.perfMeasure import PerfMeaHandler
from webapptest.base.movies import Movies

class TestPerforMovies(GaiaTestCase):
    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.app = Movies(self.marionette)
        self.app.setUp()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.item)
        self.perf = PerfMeaHandler(self.marionette.device_serial)

    def test_movies_launch(self):
        self.perf.startmea('test_movies_launch','Movies')
        self.app.launch()
        self.app.wait_for_element_displayed(*self.app.item)
        self.perf.stopmea()

    def test_movies_play_a_movie(self):
        self.perf.startmea('test_movies_play_a_movie','Movies')
        self.app.play_movie()
        self.app.is_element_displayed(*self.app.singleViewProgress)
        self.perf.stopmea()

    