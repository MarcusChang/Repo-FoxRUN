
import time
from gaiatest import GaiaTestCase
from webapptest.base.album import Album

class TestUiAlbum(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.app = Album(self.marionette)
        self.app.setUp()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.item)

    def test_album_image_loaded(self):
        self.assertTrue(self.app.is_elements_displayed(*self.app.item), 'the list is not empty')

    def test_album_single_picture_view(self):
        self.assertTrue(self.app.main_to_single(), 'full screen image should be displayed')
        self.assertTrue(self.app.single_tap_show_back(), 'back button should be displayed')
        result = self.app.single_flick()
        self.assertNotEqual(result[0], result[1], "swipe to next image")
        self.assertTrue(self.app.single_to_main(), 'the list is not empty')
