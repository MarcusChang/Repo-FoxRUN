
var Util = require('../../util'),
    assert = require('chai').assert;

var Selector = {
    wrapper: '#wrapper',
    scroller: '#scroller',
    row: '.row'
};

var APPNAMEFULL = 'Infinite scroll demo';
var URL = 'file://' + __dirname + '/../../../platform_apps/infinite-scroll/index.html';

marionette('Infinite scroll demo ', function() {
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
        const LOOP = 5;
        const APPNAME = 'Infinite scroll';
        app.wait(3 * 1000);
        var results = [];

        assert.ok(app.findElements(Selector.row).length > 0, 'the list is not empty');
        var count = 0, countInc = 0;
        var time = 0, timeInc = 0;
        var distance = 0, distanceInc = 0;
        var totalDistance = 0, totalFps = 0;
        for (var i = 0; i < LOOP; i++) {
            distance = app.findElement(Selector.scroller).location().y, distanceInc = 0;
            app.flick2('up', app.findElement(Selector.wrapper));
            count = app.client.executeScript("return window.wrappedJSObject.mozPaintCount;\n");
            time = new Date().getTime();
            app.wait(200);

            countInc = app.client.executeScript("return window.wrappedJSObject.mozPaintCount;\n") - count;
            timeInc = new Date().getTime() - time;
            distanceInc = app.findElement(Selector.scroller).location().y - distance;
            /*results.push({
                fps: Math.round(countInc * 1000 / timeInc),
                distance: -Math.round(distanceInc),
                memInfo: app.getPerfInfo(APPNAME)
            });*/
            var info;
            if (app.host == Util.HOST_BROWSER) {
                info = {};
            } else {
                info = app.getPerfInfo(APPNAME);
            }
            info.scrollDistance = -Math.round(distanceInc);
            info.fps = Math.round(countInc * 1000 / timeInc);
            results.push(info);
            totalDistance += info.scrollDistance;
            totalFps += info.fps;
            app.wait(2000);
        }

        var output = {
            app: APPNAME,
            platform: app.host,
            average: {
                cpu: results[LOOP - 1].cpu,
                uss: results[LOOP - 1].uss,
                pss: results[LOOP - 1].pss,
                rss: results[LOOP - 1].rss,
                vsize: results[LOOP - 1].vsize,
                scrollDistance: Math.round(totalDistance/LOOP),
                fps: Math.round(totalFps/LOOP),
            },
            detail: results
        }
        process.stdout.write(JSON.stringify(output, null, 2));

        if (app.host != Util.HOST_BROWSER) {
            app.closeApp();
        }
    });

});

