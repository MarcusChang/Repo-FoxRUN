var Util = require('../../util'),
    assert = require('chai').assert,
    url ,
    Selector = {
    item: 'span.swac-grid-item-content',
    menuButton: '#header .swac-actions',
    menuOverlay: '#menu',
    navButton: 'a.swac-action-nav',
    drawer: '.swac-drawer',
    drawerItem: '.swac-drawer ul li a',
    singleView: '.fullscreen .swipe',
    singleViewImage: 'div.fullscreen',
    singleViewFullScreenTarget: 'div.image:nth-child(3)',
    singleViewImageNext: '.fullscreen .nextItem',
    singleViewBack: 'a.swac-action-nav'
    };


var ORIGIN = Util.CONST_APP_NAME.ORIGIN_ALBUM;
//var URL = Util.CONST_APP_NAME.URL_ALBUM_MASTER;
var URL = Util.CONST_APP_NAME.URL_ALBUM_DEV;

marionette('album ', function() {

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

    test('image loaded', function() {
        app.waitForElement(Selector.item);
        assert.ok(app.findElements(Selector.item).length > 0, Util.TESTLOG_ALBUM.IMAGELOADED_FIRSTLOGIN);
        assert.ok(app.findElements(Selector.item)[0].displayed(), Util.TESTLOG_ALBUM.IMAGELOADED_HOMEPAGE_ITEMS);

    });

    test('single picture view', function() {

        const itemToOpen = 2;
        app.findElements(Selector.item)[itemToOpen].tap();
        app.waitForElement(Selector.singleViewImage);
        assert.isTrue(app.findElement(Selector.singleViewImage).displayed(), Util.TESTLOG_ALBUM.SINGLEPICTUREVIEW_PICTURE_OPEN);

        app.findElement(Selector.singleViewImage).tap();
        app.waitForElement(Selector.singleViewBack);
        assert.isTrue(app.findElement(Selector.singleViewBack).displayed(), Util.TESTLOG_ALBUM.SINGLEPICTUREVIEW_BACKBUTTON_DISPLAYED);

        var currentImage1 = app.findElement(Selector.singleViewImage);
        console.log(currentImage1);
        app.flick("left");
        app.sleep(Util.CONST_WAIT_TIME.FOUR_SEC_SLEEP);
        app.waitForElement(Selector.singleViewImage);
        var currentImage2 = app.findElement(Selector.singleViewImage);
        console.log(currentImage2);
        assert.notEqual(currentImage1, currentImage2, Util.TESTLOG_ALBUM.SINGLEPICTUREVIEW_PICTURE_SWIPED);

        // need to wait: flick action sometimes will cause title bar animated disppear in current version.
        if (!app.findElement(Selector.singleViewBack).displayed()) {
            app.findElement(Selector.singleViewImage).tap();
            app.waitForElement(Selector.singleViewBack);
        }

        app.findElement(Selector.singleViewBack).tap();
        app.waitForElement(Selector.item);
        assert.ok(app.findElements(Selector.item).length > 0, Util.TESTLOG_ALBUM.SINGLEPICTUREVIEW_HOMEPAGE_RETURN);
    });

});

