var Util = require('../../util'),
    assert = require('chai').assert,
    url = 'https://firefox:blackswan@entrance.fx-webapps.com/',
    itemToCompare = 2,
    host,
    Selector = {
        //item: '.grid-item .grid-item-content',
        item: '.swac-grid-item .swac-grid-item-content',
        //singleViewImage: '.ng-scope div.details.ng-scope div.ng-isolate-scope img',
        //singleViewImage: '.details .ng-isolate-scope img',
        singleViewImage: 'modal.inline-preview .swac-modal .swac-header .icon img',
        //singleViewBack: '.details .action-nav'
        //singleViewBack: '.details .swac-top-bar .swac-action-nav'
        singleViewBack: 'modal.inline-preview .swac-modal .swac-header .info button.swac-close'
    };


marionette('entrance ', function() {

    var app = new Util(process.argv);
    var client;

    if (app.host == Util.HOST_BROWSER) {
        client = null;
    } else {
        client = marionette.client();

    }

    setup(function(done) {
        app.launch(client, url,done);
    });
    teardown(function(){
        app.stop();
    });


    /* Although I start app before test. it's still not stable for load image time.*/
    test('start up', function() {
        app.waitForElement(Selector.item);
        assert.isTrue(app.findElements(Selector.item).length > 0, 'the list is not empty');
        assert.isTrue(app.findElements(Selector.item)[0].displayed(),'first item should be shown');

    });

    /*change screen orientation back to portrait.
    * if in same function. the orientation change can not see*/
    test('change screen orientation', function() {

        app.waitForElement(Selector.item);

        if (app.host == Util.HOST_DEVICE) {

            app.lockScreenLandscape();
            app.waitForElement(Selector.item);
            var size1 = app.findElements(Selector.item)[itemToCompare].size();
            app.unlockScreenOrientation();
            app.wait(2*1000);


            app.lockScreenPortrait();
            app.waitForElement(Selector.item);
            var size2 = app.findElements(Selector.item)[itemToCompare].size();
            console.log("before lock size=", size1, "after lock size=", size2);
            assert.notEqual(size1.width, size2.width, "item width should not same");
            assert.notEqual(size1.height, size2.height, "item height should not same");
            app.unlockScreenOrientation();
        }

    });

    test('single picture view', function() {
        const itemToOpen = 0;
        app.findElements(Selector.item)[itemToOpen].tap();
        app.waitForElement(Selector.singleViewImage);
        assert.isTrue(app.findElement(Selector.singleViewImage).displayed(),'full screen image should be displayed');
        app.findElement(Selector.singleViewBack).click();
        app.waitForElement(Selector.item);
        assert.isTrue(app.findElement(Selector.item).displayed(),'full screen image should be closed');
    });

});

