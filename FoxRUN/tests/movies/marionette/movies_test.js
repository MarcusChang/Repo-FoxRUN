var Util = require('../../util'),
    assert = require('chai').assert;

var Selector = {
    item: 'span.swac-grid-item-content',
    menuButton: 'div.swac-top-bar div.swac-actions button.open-menu',
    menuPinchIn: 'div.swac-actions .swac-top-menu-container ul.swac-top-menu li:nth-child(2) a',
    menuPinchOut: 'div.swac-actions .swac-top-menu-container ul.swac-top-menu li:nth-child(3) a',
    videoPreview: 'video#video-preview',
    singleViewPlayer: 'div#player.ng-scope',
    singleViewProgress: 'div#player div.control-area',
    singleViewProgressText: 'span.time-display.ng-binding',
    singleViewBack: 'div.swac-top-bar span.swac-action-nav'
};


var ORIGIN = Util.CONST_APP_NAME.ORIGIN_MOVIES;
var URL = Util.CONST_APP_NAME.URL_MOVIES_MASTER;
//var URL = Util.CONST_APP_NAME.URL_MOVIES_DEV;

//Precondition:
// 1, there's 2+ videos
// 2, each video length > 6 seconds
// 3, default view is top view
marionette('movies ', function() {
    var client;
    var testApp;
    var app = new Util(process.argv);
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

    teardown(function() {
        app.stop();
    });

    test('start up', function() {
        const itemToCompare = 1;
        app.waitForElement(Selector.item);
        //wait for movies home page loading
        app.wait(Util.CONST_WAIT_TIME.FIVE_SEC_WAIT);
        assert.ok(app.findElements(Selector.item).length > 0, Util.TESTLOG_MOVIES.STARTUP_FIRSTLOGIN);

        var size0 = app.findElements(Selector.item)[itemToCompare].size();

        //switch different view to check the item size not same
        app.findElement(Selector.menuButton).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.menuPinchOut).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.item);
        var size1 = app.findElements(Selector.item)[itemToCompare].size();
        assert.notEqual(size0.width, size1.width, Util.TESTLOG_MOVIES.STARTUP_HOMEPAGE_PINCHOUT_1);

        app.findElement(Selector.menuButton).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.menuPinchOut).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.item);
        var size2 = app.findElements(Selector.item)[itemToCompare].size();
        assert.notEqual(size1.width, size2.width, Util.TESTLOG_MOVIES.STARTUP_HOMEPAGE_PINCHOUT_2);

        app.findElement(Selector.menuButton).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.menuPinchOut).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.item);
        var size3 = app.findElements(Selector.item)[itemToCompare].size();
        assert.notEqual(size2.width, size3.width, Util.TESTLOG_MOVIES.STARTUP_HOMEPAGE_PINCHOUT_3);

        app.findElement(Selector.menuButton).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.menuPinchIn).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.item);
        var size4 = app.findElements(Selector.item)[itemToCompare].size();
        assert.notEqual(size3.width, size4.width, Util.TESTLOG_MOVIES.STARTUP_HOMEPAGE_PINCHIN_1);

        app.findElement(Selector.menuButton).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.menuPinchIn).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.item);
        var size5 = app.findElements(Selector.item)[itemToCompare].size();
        assert.notEqual(size4.width, size5.width, Util.TESTLOG_MOVIES.STARTUP_HOMEPAGE_PINCHIN_2);

        app.findElement(Selector.menuButton).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.menuPinchIn).click();
        app.sleep(Util.CONST_WAIT_TIME.ONE_SEC_SLEEP);
        app.waitForElement(Selector.item);
        var size6 = app.findElements(Selector.item)[itemToCompare].size();
        assert.notEqual(size5.width, size6.width, Util.TESTLOG_MOVIES.STARTUP_HOMEPAGE_PINCHIN_3);

    });

    test('play a movie', function() {
        const itemToOpen = 2;
        const start = "00:00";

        //tap a item to play
        app.findElements(Selector.item)[itemToOpen].click();
        app.waitForElement(Selector.singleViewPlayer);
        assert.isTrue(app.findElement(Selector.singleViewPlayer).displayed(), Util.TESTLOG_MOVIES.PLAYAMOVIE_SINGLEVIEWPLAYER_DISPLAYED);
        assert.isTrue(app.findElement(Selector.singleViewProgress).displayed(), Util.TESTLOG_MOVIES.PLAYAMOVIE_SINGLEVIEWPROGRESS_DISPLAYED);

        //wait to check the play progress
        app.wait(Util.CONST_WAIT_TIME.THREE_SEC_WAIT);
        var text = app.findElement(Selector.singleViewProgressText).text();
        var len = start.length;
        var current = text.substr(text.length - len, len);
        assert.isTrue(current > start, Util.TESTLOG_MOVIES.PLAYAMOVIE_SINGLEVIEWPROGRESSTEXT_COUNTING);

        //wait to check play progress hide
        app.wait(Util.CONST_WAIT_TIME.THREE_SEC_WAIT);
        assert.isFalse(app.findElement(Selector.singleViewProgressText).displayed(), Util.TESTLOG_MOVIES.PLAYAMOVIE_SINGLEVIEWPROGRESS_HIDE);


        //press video then press back key to return main screen top view and there's a video preview displayed
        app.findElement(Selector.singleViewPlayer).tap();
        app.waitForElement(Selector.singleViewBack).click();
        app.waitForElement(Selector.item);
        assert.isTrue(app.findElement(Selector.item).displayed(), Util.TESTLOG_MOVIES.PLAYAMOVIE_VIDEOPREVIEW_DISPLAYED);
    });

});

