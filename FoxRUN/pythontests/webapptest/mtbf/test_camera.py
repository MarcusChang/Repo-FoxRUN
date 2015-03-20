
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from webapptest.base.camera import Camera

class TestMtbfCamera(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.app = Camera(self.marionette)
        self.connect_to_network()
        self.app.launch()
        self.app.tap_confirm()
        self.app.wait_for_element_displayed(*self.app.video)

    def test_camera_submenu_can_be_shown(self):
         self.assertTrue(self.app.setting_menu_displayed(), 'settings sub menu is not find')
         self.assertTrue(self.app.setting_menu_tab_camera_displayed(), 'Camera settings tab body is not find')
         self.assertTrue(self.app.setting_menu_tab_video_displayed(), 'Video settings tab body is not find')
         self.assertTrue(self.app.setting_menu_tab_other_displayed(), 'Other settings tab body is not find')
         self.assertTrue(self.app.flash_mode_displayed(), 'flash mode sub menu is not find')

    def test_camera_shoot_works(self):
        self.assertTrue(self.app.capture_phone_button_works(), 'The last snapshot wrapper is not find')
        self.assertTrue(self.app.capture_video_button_works(), 'The last snapshot wrapper is not find')