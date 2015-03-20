/**
 * @fileoverview Contains some useful helper functions for driving gaia's
 *     Util application through the marionette js this.client.
 */

var Marionette = require('marionette-client');
var Actions = require('marionette-client').Actions;
var MemInfo = require('./performance/meminfo.js');
var execSync = require('./performance/exec-sync.js');
var fs = require('fs');

/**
 * Util.CONST_WAIT_TIME : Contains the app.sleep() / app.wait() const parameters.
 * Used for set the sleep & wait time internal.
 */

Util.CONST_WAIT_TIME = {
    ONE_SEC_SLEEP: 1,
    ONE_SEC_WAIT: 1000,
    TWO_SEC_SLEEP: 2,
    TWO_SEC_WAIT: 2000,
    THREE_SEC_SLEEP: 3,
    THREE_SEC_WAIT: 3000,
    FOUR_SEC_SLEEP: 4,
    FOUR_SEC_WAIT: 4000,
    FIVE_SEC_SLEEP: 5,
    FIVE_SEC_WAIT: 5000
};

/**
 * Util.CONST_APP_NAME : Contains the app.launch() const parameters.
 * Used for locate the target app for launch.
 */

Util.CONST_APP_NAME = {
    ORIGIN_ALBUM: 'Album',
    ORIGIN_WALKMAN: 'Walkman',
    ORIGIN_MOVIES: 'Movies',
    ORIGIN_CAMERA:'SOMC Camera',

    URL_ALBUM_MASTER: 'https://firefox:blackswan@album.fx-webapps.com',
    URL_ALBUM_DEV: 'https://firefox:blackswan@album-develop.fx-webapps.com',
    URL_WALKMAN_MASTER: 'https://firefox:blackswan@walkman.fx-webapps.com',
    URL_WALKMAN_DEV: 'https://firefox:blackswan@walkman-develop.fx-webapps.com',
    URL_MOVIES_MASTER: 'https://firefox:blackswan@movies.fx-webapps.com',
    URL_MOVIES_DEV: 'https://firefox:blackswan@movies-develop.fx-webapps.com',
    URL_CAMERA_MASTER:'https://firefox:blackswan@camera.fx-webapps.com',
    URL_CAMERA_DEV:'https://firefox:blackswan@camera-develop.fx-webapps.com'
};

/**
 * Util.TESTLOG_ALBUM : Contains all test logs for album_test.js asserts.
 * Used for assign the album test output msg for chai.js assert function.
 */

Util.TESTLOG_ALBUM = {
    IMAGELOADED_FIRSTLOGIN: '[ASSERT OK] the list is not empty',
    IMAGELOADED_HOMEPAGE_ITEMS: '[ASSERT OK] first item should be shown',

    SINGLEPICTUREVIEW_PICTURE_OPEN: '[ASSERT ISTRUE] full screen image should be displayed',
    SINGLEPICTUREVIEW_BACKBUTTON_DISPLAYED: '[ASSERT ISTRUE] back button should be displayed',
    SINGLEPICTUREVIEW_PICTURE_SWIPED: '[ASSERT NOTEQUAL] swipe to next image',
    SINGLEPICTUREVIEW_HOMEPAGE_RETURN: '[ASSERT OK] the list is not empty'
};


/**
 * Util.TESTLOG_WALKMAN : Contains all test logs for walkman_test.js asserts.
 * Used for assign the walkman test output msg for chai.js assert function.
 */

Util.TESTLOG_WALKMAN = {
    LOADSTARTPAGE_FIRSTLOGIN: '[ASSERT ISTRUE] the list is not empty',
    LOADSTARTPAGE_HOMEPAGE_ITEMS: '[ASSERT ISTRUE] first item should be shown',
    LOADSTARTPAGE_TOPBAR_FIXED: '[ASSERT EQUAL] top transparent bar should be fixed when scroll',

    PLAYAMUSICTRACK_DRAWER_DISPLAYED: '[ASSERT ISTRUE] drawer should be shown',
    PLAYAMUSICTRACK_TRACKS_NOTEMPTY: '[ASSERT ISTRUE] the track list is not empty',
    PLAYAMUSICTRACK_TRACKS_MINIPLAYER_PLAY: '[ASSERT ISTRUE] mini player should in play state',
    PLAYAMUSICTRACK_TRACKS_MINIPLAYER_PAUSE: '[ASSERT ISTRUE] mini player should in pause state',
    PLAYAMUSICTRACK_DRAWER_DISPLAYED_AGAIN: '[ASSERT ISTRUE] drawer should be shown again',
    PLAYAMUSICTRACK_DRAWER_HOMEPAGE_ITEMS: '[ASSERT ISTRUE] first item should be shown',

    NAVIGATEUSINGDRAWERMENU_DRAWER_DISPLAYED: '[ASSERT ISTRUE] drawer should be shown',
    NAVIGATEUSINGDRAWERMENU_PLAYLISTS_ADDBUTTON_DISPLAYED: '[ASSERT ISTRUE] play list view should be shown',
    NAVIGATEUSINGDRAWERMENU_DRAWER_DISPLAYED_AGAIN: '[ASSERT ISTRUE] drawer should be shown again',
    NAVIGATEUSINGDRAWERMENU_DRAWER_HOMEPAGE_ITEMS: '[ASSERT ISTRUE] first item should be shown'
};


/**
 * Util.TESTLOG_MOVIES : Contains all test logs for movies_test.js asserts.
 * Used for assign the movies test output msg for chai.js assert function.
 */

Util.TESTLOG_MOVIES = {
    STARTUP_FIRSTLOGIN: '[ASSERT OK] the list is not empty',
    STARTUP_HOMEPAGE_PINCHOUT_1: '[ASSERT NOTEQUAL] item width should not same after pinch out 1',
    STARTUP_HOMEPAGE_PINCHOUT_2: '[ASSERT NOTEQUAL] item width should not same after pinch out 2',
    STARTUP_HOMEPAGE_PINCHIN_1: '[ASSERT NOTEQUAL] item width should not same after pinch in 1',
    STARTUP_HOMEPAGE_PINCHIN_2: '[ASSERT NOTEQUAL] item width should not same after pinch in 2',
    STARTUP_HOMEPAGE_PINCHIN_3: '[ASSERT NOTEQUAL] item width should not same after pinch in 3',
    STARTUP_HOMEPAGE_PINCHOUT_3: '[ASSERT NOTEQUAL] item width should not same after pinch out 3',

    PLAYAMOVIE_SINGLEVIEWPLAYER_DISPLAYED: '[ASSERT ISTRUE] full screen video should be displayed',
    PLAYAMOVIE_SINGLEVIEWPROGRESS_DISPLAYED: '[ASSERT ISTRUE] video progress should be displayed',
    PLAYAMOVIE_SINGLEVIEWPROGRESSTEXT_COUNTING: '[ASSERT ISTRUE] video should be playing',
    PLAYAMOVIE_SINGLEVIEWPROGRESS_HIDE: '[ASSERT ISFALSE] video progress should not be displayed',
    PLAYAMOVIE_VIDEOPREVIEW_DISPLAYED: '[ASSERT ISTRUE] video preview should be displayed'
};


/**
 * Util.TESTLOG_CAMERA : Contains all test logs for camera_test.js asserts.
 * Used for assign the movies test output msg for chai.js assert function.
 */
Util.TESTLOG_CAMERA = {
    CASE_SUBMENU_LAUNCHING_VIDEO: '[ASSERT ISTRUE] launching camera failed',
    CASE_SUBMENU_SETTING_BUTTON: '[ASSERT ISTRUE] Setting button is not find',
    CASE_SUBMENU_SETTING_SHOWN: '[ASSERT ISTRUE] settings sub menu is not find',
    CASE_SUBMENU_CAMERA_SETTING_TAB: '[ASSERT ISTRUE] Camera settings tab is not find',
    CASE_SUBMENU_CAMERA_SETTING_SHOWN: '[ASSERT ISTRUE] Camera settings tab body is not find',
    CASE_SUBMENU_VIDEO_SETTING_TAB: '[ASSERT ISTRUE] Video settings tab is not find',
    CASE_SUBMENU_VIDEO_SETTING_SHOWN: '[ASSERT ISTRUE] Video settings tab body is not find',
    CASE_SUBMENU_OTHER_SETTING_TAB: '[ASSERT ISTRUE] Other settings tab is not find',
    CASE_SUBMENU_OTHER_SETTING_SHOWN: '[ASSERT ISTRUE] Other settings tab body is not find',

    CASE_SHOOT_CAPTURE_PHONE_BUTTON: '[ASSERT ISTRUE] Capture phone button is not find',
    CASE_SHOOT_LAST_SNAPSHOT_POPUP: '[ASSERT ISTRUE] The last snapshot wrapper is not find',
    CASE_SHOOT_CAPTURE_VIDEO_BUTTON: '[ASSERT ISTRUE] The capture video button is not find',
    CASE_SHOOT_CAPTURE_VIDEO_RECORDING: '[ASSERT ISTRUE] The video is not recording'
};

/**
 * @constructor
 *  common class.
 */
function Util(args) {
    this.parseArgs(args);
}

module.exports = Util;

Util.HOST_DEVICE = 'marionette-device-host';
Util.HOST_BROWSER = 'marionette-firefox-host';
Util.HOST_B2GDESKTOP = 'marionette-b2gdesktop-host';
Util.LAUNCH_TIMEOUT = 30*1000;//launch app wait time


Util.prototype = {
    /**
     * Marionette host to use.
     * @type {Marionette.host}
     */
    host: null,

    /**
     * Marionette this.client to use.
     * @type {Marionette.this.client}
     */
    client: null,

    /**
     * Marionette this.client to use.
     * @type {Marionette.this.client}
     */
    origin: null,

    /**
     * Find some element given its name like 'addEventButton' or 'weekButton'.
     *
     * @param {string} name of some Util element.
     * @return {Marionette.Element} the element.
     */
    findElement: function(name) {
        return this.client.findElement(name);
    },

    /**
     * Find some elements given their name.
     *
     * @param {string} name of some Util elements.
     * @return {Array.<Marionette.Element>} the element.
     */
    findElements: function(name) {
        return this.client.findElements(name);
    },

    /**
     * @param {string} name of some Util element.
     * @return {Marionette.Element} the element.
     */
    waitForElement: function(name) {
        return this.client.helper.waitForElement(name);
    },

    /**
     * time out.
     *
     * @param {timeout} [int] millisecond
     */
    wait: function(timeout) {
        return this.client.helper.wait(timeout);
    },

    /**
     * time out.
     *
     * @param {timeout} [int] second
     */
    sleep: function(timeout) {
        execSync('sleep ' + timeout, true);
    },

    /**
     * @param {Marionette.Element|string} parent element or name of element.
     * @param {string} child name of child element.
     */
    waitForChild: function(parent, child) {
        return this.client.helper.waitForChild(parent, child);
    },

    /**
     * Swipe on a panel.
     * If no element param, it will swipe on the body element.
     *
     * @param {Marionette.Element} [element] the panel element.
     */
    swipe: function(element) {
        var bodySize = this.client.executeScript(function() {
            return {
                height: document.body.clientHeight,
                width: document.body.clientWidth
            };
        });

        // (x1, y1) is swipe start.
        // (x2, y2) is swipe end.
        const x1 = bodySize.width * 0.2,
            y1 = bodySize.height * 0.2,
            x2 = 0,
            y2 = bodySize.height * 0.2;

        var panel = element || this.client.findElement('body');
        this.actions
            .flick(panel, x1, y1, x2, y2)
            .perform();
    },

    /**
     * flick on a element.
     *
     * @param {direction} [element] the flick element direction.
     */

    flick: function(direction, element) {
        var bodySize = this.client.executeScript(function() {
            return {
                height: document.body.clientHeight,
                width: document.body.clientWidth
            };
        });
        // (x1, y1) is swipe start.
        // (x2, y2) is swipe end.
        var x1 = Math.ceil(bodySize.width * 0.5);
        var y1 = Math.ceil(bodySize.height * 0.5);
        var x2 = x1;
        var y2 = y1;
        switch (direction) {
            case 'up':
                y2 = Math.ceil(bodySize.height * 0.2);
                break;
            case 'down':
                y2 = Math.ceil(bodySize.height * 0.8);
                break;
            case 'left':
                x2 = Math.ceil(bodySize.width * 0.2);
                break;
            case 'right':
                x2 = Math.ceil(bodySize.width * 0.8);
                break;
            default :
                break;
        }

        var panel = element || this.client.findElement('body');
        this.actions
            .flick(panel, x1, y1, x2, y2)
            .perform();
        //this.client.helper.waitForElement('body');
    },

    /**
     * flick on a element.
     *
     * @param {direction} [element] the flick element direction.
     */

    flick2: function(direction, element) {
        const WAIT = 30.0 / 1000;
        const OFFSET = 80;
        var x = 0, y = 0;
        switch (direction) {
            case 'up':
                y = -OFFSET;
                break;
            case 'down':
                y = OFFSET;
                break;
            case 'left':
                x = -OFFSET;
                break;
            case 'right':
                x = OFFSET;
                break;
            default :
                break;
        }

        var panel = element || this.client.findElement('body');
        var action = new Actions(this.client);
        action.press(panel).moveByOffset(x, y).wait(WAIT).release().perform();
        //this.client.helper.waitForElement('body');
    },

    getPerfInfo: function(appName) {
        var meminfo = MemInfo.meminfo();
        var info = null;
        meminfo.some(function(element) {
            if(element.NAME == appName) {
                info = element;
                return info;
            }
        });

        if (!info) {
            return null;
        }

        return {
            cpu: parseFloat(info['CPU(s)']),
            uss: parseFloat(info.USS),
            pss: parseFloat(info.PSS),
            rss: parseFloat(info.RSS),
            vsize: parseFloat(info.VSIZE)
        };
    },

    /**
     * scroll window.
     *
     * @param {pos} [pos] scroll distance.
     */
    scrollTo: function(pos) {
        var posarr = new Array();
        posarr[0] = pos;
        this.client.executeScript("window.scrollTo(0, arguments[0]);",script_args=posarr);
    },

    /**
     * get attribute of element.
     *
     * @param {cssString, attributeString} [cssString] the css of element,[attributeString] which is
     * attribute of element.
     */
    getAttribute: function(cssString, attributeString) {
        const delimeter = ';',
            delimeter2 = ':';
        var attributes = cssString.split(delimeter);
        var l = attributes.length;
        for ( var i = 0; i < l; i++) {
            var trimed =attributes[i].trim();
            var pos =trimed.indexOf(delimeter2);
            var propertyName =trimed.substring(0, pos);
            if (propertyName == attributeString) {
                return trimed.substring(pos + 1).trim();
            }
        }
    },

    /**
     * get attribute of element.
     *
     * @param {element, attribute} [element] the  element id,[attribute] which is
     * attribute of element.
     */
    getCssAttribute: function(element, attribute) {
        var style = this.findElement(element).getAttribute('style');
        return this.getAttribute(style, attribute);
    },

    /**
     * get the host  we are testing.
     *
     * @param {name} [name] make file test argv.
     */
    parseArgs: function(name) {
        var l = name.length;
        for ( var i = 0; i < l; i++) {
            if (name[i] == Util.HOST_DEVICE) {
                this.host = Util.HOST_DEVICE;
                break;
            } else if (name[i] == Util.HOST_B2GDESKTOP) {
                this.host = Util.HOST_B2GDESKTOP;
                break;
            } else if (name[i].indexOf(Util.HOST_BROWSER) >= 0) {
                this.host = Util.HOST_BROWSER;
                break;
            }
        }
        if (this.host == null) {
            //set default host to device
            this.host = Util.HOST_DEVICE;
        }
        return this.host;
    },

    /**
     * close app.
     */
    closeApp: function() {
        this.client.apps.close(this.origin);
    },

    /**
     * unlock screen.
     */
    unlockScreen: function() {
        this.client.executeScript(fs.readFileSync(__dirname + '/gaia_lock_screen.js') + '\n'
                + 'window.wrappedJSObject.GaiaLockScreen = GaiaLockScreen;\n');
        this.client.executeScript(function() {
            window.wrappedJSObject.GaiaLockScreen.unlock();
        });
    },

    /**
     * launch app by app name
     *
     * @param {name} [name] make file test argv.
     */
    launchByName: function(name) {
        this.client.executeScript(fs.readFileSync(__dirname + '/gaia_apps.js') + '\n'
                + 'window.wrappedJSObject.GaiaApps = GaiaApps;\n');
        this.client.executeScript(function() {
            window.wrappedJSObject.GaiaApps.launchWithName(arguments[0]);
        },script_args=[name]);
        // wait for 2 second to wait app launched. Maybe can use callback replace.
        this.sleep(Util.CONST_WAIT_TIME.TWO_SEC_SLEEP);
        this.origin = this.client.executeScript(function() {
            return window.wrappedJSObject.GaiaApps.getActiveApp().origin;
        });
    },

    /**
     * Start the app
     *
     * @param {marionetteclient, url,  done}
     * marionetteclient:if the target is desktop browser, this.client should be null,otherwise is not null.
     * url: the origin of an app on device or the url of app on browser
     * done is callback
     */
    launch: function(marionetteclient, url, done, isolate) {

        if (this.host != Util.HOST_BROWSER) {
            this.client = marionetteclient.scope({ searchTimeout: 20 * 1000 });
            this.actions = new Marionette.Actions(this.client);

            this.unlockScreen();
            //this.client.apps.launch(url);
            this.launchByName(url);
            //wait for the app launched successfully.
            this.sleep(Util.CONST_WAIT_TIME.TWO_SEC_SLEEP);
            this.client.apps.switchToApp(this.origin);

            if (isolate) {
                //wait for the app launched and the image | video | track are loaded.
                this.sleep(Util.CONST_WAIT_TIME.THREE_SEC_SLEEP);
            } else {
                // Currently app start very slow sometimes, it can also affect other applications test.
                this.sleep(Util.CONST_WAIT_TIME.FIVE_SEC_SLEEP);
                //Wait for the document body to know we're really 'launched'.
                this.client.helper.waitForElement('body');
            }
            done();
        } else {
            var self = this;
            var driver = new Marionette.Drivers.TcpSync();

            self.client =  new Marionette.Client(driver);
            self.client.plugin('helper', require('marionette-helper'));
            self.client = self.client.scope({ searchTimeout: 30 * 1000 });

            driver.connect(function(err) {
                if (err) {
                    console.log('driver connect error:');
                }

                self.client.startSession(function () {

                    self.actions = new Marionette.Actions(self.client);
                    self.client.goUrl(url);
                    self.wait(Util.LAUNCH_TIMEOUT);
                    done();
                });
            });
        }
    },
    /**
     * disconnect the session
     *
     */
    stop:function()
    {
        if (this.host == Util.HOST_BROWSER) {
            this.client.deleteSession();
        }
    },

    /**
     * handle login dialog
     *
     */
    makePrecondition:function(url)
    {
        var handled = true;
        this.client.apps.launch(url);
        this.client.apps.switchToApp(url);
        //sometimes the login dialog will take long time to show.
        this.sleep(Util.CONST_WAIT_TIME.FIVE_SEC_SLEEP);
        this.client.switchToFrame();
        try {
            var element = this.findElement("div[id*='AuthenticationDialog']");
            var user = this.findElement(".authentication-dialog-http-username-input");
            user.clear();
            user.sendKeys("firefox");
            var pwd = this.findElement(".authentication-dialog-http-password-input");
            pwd.clear()
            pwd.sendKeys("blackswan");
            this.wait(Util.CONST_WAIT_TIME.ONE_SEC_WAIT);
            this.findElement(".authentication-dialog-http-authentication-ok.affirmative").tap();
            this.wait(Util.CONST_WAIT_TIME.ONE_SEC_WAIT);
        } catch(err) {
            handled = false;
        }
	if (handled) {
            //this.wait(Util.CONST_WAIT_TIME.TWO_SEC_WAIT);
            this.client.apps.close(url);
            this.client.switchToFrame();
        }

        return handled;
    },
    /**
     * lock screen for Landscape
     *
     */
    lockScreenLandscape: function() {
        var success = this.client.executeScript("return screen.mozLockOrientation('landscape-primary');");
    },
    /**
     * lock screen for Portrait
     *
     */
    lockScreenPortrait: function() {
        var success = this.client.executeScript("return screen.mozLockOrientation('portrait-primary');");
    },
    /**
     * unlock screen
     *
     */
    unlockScreenOrientation: function() {
        var success = this.client.executeScript("return screen.mozUnlockOrientation();");
    }

};
