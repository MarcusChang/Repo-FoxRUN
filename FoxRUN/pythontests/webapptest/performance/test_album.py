
from gaiatest import GaiaTestCase
from webapptest.mixins.perfMeasure import PerfMeaHandler
from webapptest.base.album import Album

class TestPerforAlbum(GaiaTestCase):
    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.app = Album(self.marionette)
        self.app.setUp()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.item)
        self.perf = PerfMeaHandler(self.marionette.device_serial)
    def test_album_launch(self):
        self.perf.startmea('test_album_setUp','Album')
        self.app.launch()
        self.app.wait_for_element_displayed(*self.app.item)
        self.perf.stopmea()

    def test_album_image_loaded(self):
        self.perf.startmea('test_album_image_loaded','Album')
        self.app.is_elements_displayed(*self.app.item)
        self.perf.stopmea()

    def test_album_single_picture_view(self):
        self.perf.startmea('test_album_single_picture_view','Album')
        self.app.main_to_single()
        self.app.single_tap_show_back()
        self.app.single_flick()
        self.perf.stopmea()
