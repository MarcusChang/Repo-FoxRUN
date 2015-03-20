var fs = require('fs'),
    util = require('util'),
    assert = require('assert'),
    username='firefox',
    paswd='blackswan';

/* This is a helper to for perftesting apps. */
function PerfTestApp(client) {

  var arr = mozTestInfo.appPath.split('/');

  manifestPath = arr[0];
  entryPoint = arr[1];

  this.origin = util.format('https://%s.fx-webapps.com',manifestPath);

  this.entryPoint = entryPoint;
  this.client = client;
  this.skip = false;

}

module.exports = PerfTestApp;

PerfTestApp.prototype = {

  selectors: {},

  /** the Webapp instance. */
  instance: null,

  PERFORMANCE_ATOM: 'window.wrappedJSObject.PerformanceHelperAtom',

  defaultCallback: function() {
  },

  /**
   * Launches app, switches to frame, and waits for it to be loaded.
   */
  launch: function() {
     var self = this;
     this.client.apps.launch(this.origin, this.entryPoint, function(err, app) {
     if (app) {
         self.instance = app;
     }

     });

     this.client.apps.switchToApp(this.origin);
     this.client.helper.waitForElement('body');

  },

  close: function() {
    this.client.apps.close(this.origin);
  },

  /**
   * Finds a named selector.
   *
   * @param {String} name aliased css selector.
   * @return {String} css selector.
   */
  selector: function(name) {
    var selector;
    if (!(name in this.selectors)) {
      throw new Error('unknown element "' + name + '"');
    }

    return this.selectors[name];
  },

  /**
   * Find a named selector.
   * (see .selectors)
   *
   *
   *    var dayView = app.element('dayView');
   *
   *
   * @param {String} name selector alias.
   * @param {Function} [callback] uses driver by default.
   */
  element: function(name, callback) {
    this.client.findElement(this.selector(name), callback);
    },

  waitForElement: function(name) {
        return this.client.helper.waitForElement(name);
    },
  /**
     * time out.
     *
     * @param {length} [length] millisecond
     */
    wait: function(timeout) {
        return this.client.helper.wait(timeout);
    },
  /**
     * initialize  PerformanceHelperAtom.
     */
  observePerfEvents: function() {

    this.client.executeScript(
      fs.readFileSync('./tests/util/performance/performance_helper_atom.js') + '\n'
    );

   },
  /**
     * get performance info
     * @param {stopEventName} [stopEventName] is listen performance event name
     * @param {Function} [callback] get performance value.
     */
  waitForPerfEvents: function(stopEventName, callback) {
        var client = this.client;
        var self = this;

        var posarr = new Array();
        posarr[0] = stopEventName;

        var runResults = client.executeScript(
            'return ' + self.PERFORMANCE_ATOM + '.getMeasurements(arguments[0]);',script_args=posarr
        );

        client.executeScript(
             self.PERFORMANCE_ATOM + '.unregister();'
        );

        if(callback)
        {
            callback(runResults);
        }

  },
    makePrecondition:function()
    {
        var handled = true;
        var element = null;
        this.client.apps.launch(this.origin);
        this.client.apps.switchToApp(this.origin);

        //sometimes the login dialog will take long time to show.
        this.wait(5 * 1000);
        this.client.switchToFrame();
        try {
            element = this.client.helper.waitForElement("div[id*='AuthenticationDialog']");

            var user = this.client.findElement(".authentication-dialog-http-username-input");
            user.clear();
            user.sendKeys(username);

            this.wait(2 * 1000);
            var pwd = this.client.findElement(".authentication-dialog-http-password-input");
            pwd.clear()
            pwd.sendKeys(paswd);

            this.wait(1 * 1000);
            this.client.findElement(".authentication-dialog-http-authentication-ok.affirmative").tap();
            this.wait(1 * 1000);
        } catch(err) {
            console.log('err is: ',err);
            handled = false;

        }
        if (handled) {
            //this.wait(2 * 1000);
            this.client.apps.close(this.origin);
            this.client.switchToFrame();
        }

        return handled;
    }
};
