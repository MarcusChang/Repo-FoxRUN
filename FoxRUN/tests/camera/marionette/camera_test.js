var Util = require('../../util'),
    assert = require('chai').assert,
    url ,
    Selector = {
        video:'body',
        settingsButton:'span.sfi-cam-options',
        settingsSubMenu:'div.modal-dialog.modal-option',
        settingsSubMenuTabCamera: 'span.sfi-cam-camera',
        settingsSubMenuTabVideo: 'span.sfi-cam-video',
        settingsSubMenuTabOther: 'span.sfi-cam-settings',
        CameraSubMenuTabBody: 'div#setting_pane_photo.tab-pane.active',
        VideoSubMenuTabBody: 'div#setting_pane_video.tab-pane.active',
        OtherSubMenuTabBody: 'div#setting_pane_other.tab-pane.active',
        flashModeButton:'span.sfi-cam-flash-auto',
        flashModeSubMenu:'span.list-icon.sfi-cam-flash-auto',
        capturePhotoButton:'div#captureButton.icon-capture-photo',
        captureVideoButtonOFF:'div.icon-capture-video',
        captureVideoButtonON:'div.icon-capture-video-rec-pressed',
        lastSnapshotWrapperPhoto: 'div.last-snapshot-wrapper'
    };

var ORIGIN = Util.CONST_APP_NAME.ORIGIN_CAMERA;
var URL = Util.CONST_APP_NAME.URL_CAMERA_MASTER;
//var URL = Util.CONST_APP_NAME.URL_CAMERA_DEV;

marionette('camera ', function() {

    var app = new Util(process.argv);
    var client;

    if (app.host == Util.HOST_BROWSER) {
        client = null;
        testApp = URL;
    } else {
        client = marionette.client();
        testApp = ORIGIN;
    }

    setup(function(done) {
            app.launch(client, testApp, done);
    });

    teardown(function(){
        app.stop();
    });

    test('Sub_menu can be shown', function() {
        app.waitForElement(Selector.video);
        assert.isTrue(app.findElement(Selector.video).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_LAUNCHING_VIDEO);

        app.waitForElement(Selector.settingsButton);
        assert.isTrue(app.findElement(Selector.settingsButton).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_SETTING_BUTTON);

        app.waitForElement(Selector.settingsButton).click();
        app.waitForElement(Selector.settingsSubMenu);
        assert.isTrue(app.findElement(Selector.settingsSubMenu).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_SETTING_SHOWN);

        assert.isTrue(app.findElement(Selector.settingsSubMenuTabCamera).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_CAMERA_SETTING_TAB);
        app.waitForElement(Selector.settingsSubMenuTabCamera).click();
        assert.isTrue(app.findElement(Selector.CameraSubMenuTabBody).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_CAMERA_SETTING_SHOWN);

        assert.isTrue(app.findElement(Selector.settingsSubMenuTabVideo).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_VIDEO_SETTING_TAB);
        app.waitForElement(Selector.settingsSubMenuTabVideo).click();
        assert.isTrue(app.findElement(Selector.VideoSubMenuTabBody).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_VIDEO_SETTING_SHOWN);

        assert.isTrue(app.findElement(Selector.settingsSubMenuTabOther).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_OTHER_SETTING_TAB);
        app.waitForElement(Selector.settingsSubMenuTabOther).click();
        assert.isTrue(app.findElement(Selector.OtherSubMenuTabBody).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_OTHER_SETTING_SHOWN);

        app.waitForElement(Selector.flashModeButton).click();
        app.sleep(Util.CONST_WAIT_TIME.TWO_SEC_SLEEP);
        app.waitForElement(Selector.flashModeSubMenu).click();

        app.waitForElement(Selector.video);
        assert.isTrue(app.findElement(Selector.video).displayed(), Util.TESTLOG_CAMERA.CASE_SUBMENU_LAUNCHING_VIDEO);
    });

    test('Shoot works',function(){

        app.waitForElement(Selector.capturePhotoButton);
        assert.isTrue(app.findElement(Selector.capturePhotoButton).displayed(), Util.TESTLOG_CAMERA.CASE_SHOOT_CAPTURE_PHONE_BUTTON);
        app.findElement(Selector.capturePhotoButton).tap();
        app.waitForElement(Selector.lastSnapshotWrapperPhoto);
        assert.isTrue(app.findElement(Selector.lastSnapshotWrapperPhoto).displayed(), Util.TESTLOG_CAMERA.CASE_SHOOT_LAST_SNAPSHOT_POPUP);

        app.waitForElement(Selector.captureVideoButtonOFF);
        assert.isTrue(app.findElement(Selector.captureVideoButtonOFF).displayed(), Util.TESTLOG_CAMERA.CASE_SHOOT_CAPTURE_VIDEO_BUTTON);
        app.findElement(Selector.captureVideoButtonOFF).tap();
        app.waitForElement(Selector.captureVideoButtonON);
        assert.isTrue(app.findElement(Selector.captureVideoButtonON).displayed(), Util.TESTLOG_CAMERA.CASE_SHOOT_CAPTURE_VIDEO_RECORDING);
        app.sleep(Util.CONST_WAIT_TIME.THREE_SEC_SLEEP);
        app.findElement(Selector.captureVideoButtonON).tap();
        assert.isTrue(app.findElement(Selector.lastSnapshotWrapperPhoto).displayed(), Util.TESTLOG_CAMERA.CASE_SHOOT_LAST_SNAPSHOT_POPUP);

    });

});