
var Util = require('../../util'),
    fs = require('fs'),
    assert = require('chai').assert;

var Selector = {
    images: '#images',
    item: 'img',
};

var APPNAMEFULL = 'Transition demo';
var URL = 'file://' + __dirname + '/../../../platform_apps/transitions-performance/index.html';

marionette('Transition demo ', function() {
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
        const APPNAME = 'Transition demo';
        app.wait(3 * 1000);
        var results = [];

        assert.ok(app.findElements(Selector.item).length > 0, 'the list is not empty');
        var count = 0, countInc = 0;
        var time = 0, timeInc = 0;
        var totalFps = 0;
        for (var i = 0; i < LOOP; i++) {
            app.findElement(Selector.images).tap();
            count = app.client.executeScript("return window.wrappedJSObject.mozPaintCount;\n");
            time = new Date().getTime();
            app.wait(200);

            countInc = app.client.executeScript("return window.wrappedJSObject.mozPaintCount;\n") - count;
            timeInc = new Date().getTime() - time;
            /*results.push({
                fps: Math.round(countInc * 1000 / timeInc),
                memInfo: app.getPerfInfo(APPNAME)
            }); */
            var info;
            if (app.host == Util.HOST_BROWSER) {
                info = {};
            } else {
                info = app.getPerfInfo(APPNAME);
            }
            info.fps = Math.round(countInc * 1000 / timeInc);
            results.push(info);
            totalFps += info.fps;
            app.wait(1 * 1000);
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


