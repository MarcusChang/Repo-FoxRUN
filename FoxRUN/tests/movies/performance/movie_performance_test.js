'use strict';

var assert = require('assert'),
    MarionetteHelper = requireGaia('/tests/util/performance/helper.js'),
    PerformanceHelper = requireGaia('/tests/util/performance/performance_helper.js'),
    APP = requireGaia('/tests/util/performance/app.js'),
    Selector = {
       item: 'body'
  };

marionette(mozTestInfo.appPath + ' >', function() {
  var client = marionette.client({
    settings: {
      'ftu.manifestURL': null
    }
  });

  setup(function() {
    this.timeout(500000);
    client.setScriptTimeout(50000);

    MarionetteHelper.unlockScreen(client);
  });

  test('Entrance rendering time >', function() {

    var app = new APP(client);
    var lastEvent = 'show-picture';

    var performanceHelper = new PerformanceHelper({
      app: app,
      lastEvent: lastEvent
    });

    performanceHelper.repeatWithDelay(function(app, next) {

      app.launch();

      performanceHelper.observe();

      app.waitForElement(Selector.item);

      performanceHelper.waitForPerfEvent(function(runResults) {
        performanceHelper.reportRunDurations(runResults);

        console.log('runResults',runResults);
        assert.ok(Object.keys(runResults).length, 'empty results');
        app.close();

      });

    });

    performanceHelper.finish();
  });
});
