
var Util = require('../../util'),
    fs = require('fs'),
    assert = require('chai').assert;

var Selector = {
    flip: '.flip-tiles',
    flip_sequentially: '.flip-tiles-sequentially',
    reset: '.reset-tiles',
    add: '.add-more-tiles',
    item: '.flip-grid-item',
};

var APPNAMEFULL = 'Flipping Tiles'
var URL = 'file://' + __dirname + '/../../../platform_apps/flipping-tiles/flipping-tiles.html';

marionette('flipping tiles ', function() {
    const APPNAME = 'Flipping Tiles';
    var client;
    var testApp;
    var app = new Util(process.argv);
    if (app.host == Util.HOST_BROWSER) {
        client = null;
        testApp = URL;
    } else {
        client = marionette.client();
        testApp = APPNAMEFULL;
    }

    setup(function(done) {
        app.launch(client, testApp, done, true);
    });

    teardown(function() {
        app.stop();
    });

    test('start up', function() {
        app.wait(3 * 1000);
        assert.ok(app.findElements(Selector.item).length > 0, 'the list is not empty');
        var imageX1 = runFullTest();
        app.findElement(Selector.add).tap();
        app.wait(1 * 1000);
        app.findElement(Selector.add).tap();
        app.wait(1 * 1000);
        var imageX3 = runFullTest();

        var output = {
            app: APPNAME,
            platform: app.host,
            imageX1Flip: imageX1[0],
            imageX1FlipSequentially: imageX1[1],
            imageX3Flip: imageX3[0],
            imageX3FlipSequentially: imageX3[1],
        };

        process.stdout.write(JSON.stringify(output, null, 2));

        if (app.host != Util.HOST_BROWSER) {
            app.closeApp();
        }
    });

    function runFullTest(element, checkTime, waitTime) {
        var element;

        element = app.findElement(Selector.flip);
        var flip = runTest (element, 700, 2 * 1000);

        element = app.findElement(Selector.flip_sequentially);
        var flips = runTest (element, 3 * 1000, 12 * 1000);
        return [flip, flips];
    };

    function runTest(element, checkTime, waitTime) {
        app.wait(3 * 1000);
        const LOOP = 3;
        var count = 0, countInc = 0;
        var time = 0, timeInc = 0;
        var totalFps = 0;
        var results = [];
        for (var i = 0; i < LOOP; i++) {
            element.tap();
            count = app.client.executeScript("return window.wrappedJSObject.mozPaintCount;\n");
            time = new Date().getTime();
            app.wait(checkTime);

            countInc = app.client.executeScript("return window.wrappedJSObject.mozPaintCount;\n") - count;
            timeInc = new Date().getTime() - time;
            /*results.push({
                fps: Math.round(countInc * 1000 / timeInc),
                memInfo: app.getPerfInfo(APPNAME)
            });*/
            var info;
            if (app.host == Util.HOST_BROWSER) {
                info = {};
            } else {
                info = app.getPerfInfo(APPNAME);
            }
            info.fps = Math.round(countInc * 1000 / timeInc);
            results.push(info);
            totalFps += info.fps;
            app.wait(waitTime);
        }
        var output = {
            average: {
                cpu: results[LOOP - 1].cpu,
                uss: results[LOOP - 1].uss,
                pss: results[LOOP - 1].pss,
                rss: results[LOOP - 1].rss,
                vsize: results[LOOP - 1].vsize,
                fps: Math.round(totalFps/LOOP),
            },
            detail: results
        }
        return output;
    };
});

