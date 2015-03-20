'use strict';

var assert = require('assert');

var App = require('./app');
var PerformanceHelper = requireGaia('/tests/util/performance/performance_helper.js');
var MarionetteHelper = requireGaia('/tests/util/performance/helper.js');



var manifestPath, entryPoint;
var arr = mozTestInfo.appPath.split('/');
manifestPath = arr[0];
entryPoint = arr[1];


marionette('startup event test > ' + mozTestInfo.appPath + ' >', function() {

  var client = marionette.client({
    settings: {
      'ftu.manifestURL': null
    }
  });
  var lastEvent = 'startup-path-done';

  var app = new App(client, mozTestInfo.appPath);
  if (app.skip) {
    return;
  }

  var performanceHelper = new PerformanceHelper({
    app: app,
    lastEvent: lastEvent
  });

  setup(function() {
    // it affects the first run otherwise
    this.timeout(500000);
    client.setScriptTimeout(50000);

    MarionetteHelper.unlockScreen(client);
  });

  test('startup >', function() {

    performanceHelper.repeatWithDelay(function(app, next) {
      
      app.launch();
      performanceHelper.observe();

      performanceHelper.waitForPerfEvent(function(runResults, error) {
        if (error) {
          app.close();
          throw error;
        } else {
          performanceHelper.reportRunDurations(runResults);
          assert.ok(Object.keys(runResults).length, 'empty results');
          app.close();
        }
      });
    });

    performanceHelper.finish();

  });

});
