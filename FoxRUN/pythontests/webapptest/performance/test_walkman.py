
from gaiatest import GaiaTestCase
from webapptest.base.walkman import Walkman
from webapptest.mixins.perfMeasure import PerfMeaHandler

class TestPerforWalkman(GaiaTestCase):
    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.app = Walkman(self.marionette)
        self.app.setUp()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.item)
        self.perf = PerfMeaHandler(self.marionette.device_serial)
    def test_walkman_launch(self):
        self.perf.startmea('test_walkman_launch','Walkman')
        self.app.launch()
        self.app.wait_for_element_displayed(*self.app.item)
        self.perf.stopmea()

    def test_walkman_play_music(self):
        self.app.show_drawer()
        self.perf.startmea('perform_walkman_play_music','Walkman')
        self.app.show_tracklist()
        self.app.press_tracklist()
        self.perf.stopmea()
