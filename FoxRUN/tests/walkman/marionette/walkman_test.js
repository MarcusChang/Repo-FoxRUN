var Util = require('../../util'),
    assert = require('chai').assert;

var Selector = {
    item: '.swac-featured .swac-layer img',
    topBar: 'div.swac-top-bar',
    drawerButton: 'div.swac-top-bar a.swac-action-nav',
    drawer: '.swac-drawer',
    drawerOverlay: '.overlay',
    drawerPlaylist: 'i.swac-icon.drawer-playlists',
    drawerHome: 'i.swac-icon.drawer-home',
    drawerAlbum: 'i.swac-icon.drawer-albums',
    drawerTracks: 'i.swac-icon.drawer-tracks',
    playlistEdit: 'button.icon-edit',
    playlistAdd: 'div.toolbar a',
    playlistAddSave: 'div.input-addon button.primary-action',
    playlistAddCancel: '.main-content .content form.form-group button .icon-delete',
    playlistAddArea: '.main-content .content form.playlistAddform-group',
    playlistSmartList: 'ul.track-list',
    playlistUserList: 'ul.track-list(2)',
    albumListItem: '.sorted-list ul.track-list liplaylistAdd a',
    trackListHeader: '.main-content .header',
    trackListItem: 'div.content ul.track-list li a',
    miniPlayer: '.miniplayer',
    miniPlayerPlay: '.miniplayer .icon-musiccontrol_play',
    miniPlayerPause: '.miniplayer .icon-musiccontrol_pause'
};


var ORIGIN = Util.CONST_APP_NAME.ORIGIN_WALKMAN;
var URL = Util.CONST_APP_NAME.URL_WALKMAN_MASTER;
//var URL = Util.CONST_APP_NAME.URL_WALKMAN_DEV;

//verified on browser. not in device due to currently walkman can not run in device.
//can not pass sometimes due to performance issue. expected page can not display.
marionette('walkman ', function() {

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

    test('load start page', function() {
        app.waitForElement(Selector.item);
        assert.isTrue(app.findElements(Selector.item).length > 0, Util.TESTLOG_WALKMAN.LOADSTARTPAGE_FIRSTLOGIN);
        assert.isTrue(app.findElements(Selector.item)[0].displayed(), Util.TESTLOG_WALKMAN.LOADSTARTPAGE_HOMEPAGE_ITEMS);
        var topBarY = app.findElement(Selector.topBar).location().y;
        app.scrollTo(30);
        var topBarY1 = app.findElement(Selector.topBar).location().y;
        assert.equal(topBarY, topBarY1, Util.TESTLOG_WALKMAN.LOADSTARTPAGE_TOPBAR_FIXED);
        app.scrollTo(0);
    });

    test('play a music track', function() {
        app.findElement(Selector.drawerButton).click();
        app.waitForElement(Selector.drawer);
        assert.isTrue(app.findElement(Selector.drawer).displayed(), Util.TESTLOG_WALKMAN.PLAYAMUSICTRACK_DRAWER_DISPLAYED);

        //show track list view
        app.waitForElement(Selector.drawerTracks).tap();
        app.waitForElement(Selector.trackListItem);
        assert.isTrue(app.findElements(Selector.trackListItem).length > 0, Util.TESTLOG_WALKMAN.PLAYAMUSICTRACK_TRACKS_NOTEMPTY);

        //press a track list and play 2 seconds
        app.findElement(Selector.trackListItem).click();
        app.waitForElement(Selector.miniPlayerPause);
        assert.isTrue(app.findElement(Selector.miniPlayerPause).displayed(), Util.TESTLOG_WALKMAN.PLAYAMUSICTRACK_TRACKS_MINIPLAYER_PLAY);

        //press pause buttondrawerButton
        app.waitForElement(Selector.miniPlayerPause).click();
        app.waitForElement(Selector.miniPlayerPlay);
        assert.isTrue(app.findElement(Selector.miniPlayerPlay).displayed(), Util.TESTLOG_WALKMAN.PLAYAMUSICTRACK_TRACKS_MINIPLAYER_PAUSE);

        //tap drawer button again
        app.findElement(Selector.drawerButton).click();
        app.waitForElement(Selector.drawer);
        assert.isTrue(app.findElement(Selector.drawer).displayed(), Util.TESTLOG_WALKMAN.PLAYAMUSICTRACK_DRAWER_DISPLAYED_AGAIN);

        //tap walkman menu to show main screen
        app.waitForElement(Selector.drawerHome).tap();
        app.waitForElement(Selector.item);
        assert.isTrue(app.findElements(Selector.item)[0].displayed(), Util.TESTLOG_WALKMAN.PLAYAMUSICTRACK_DRAWER_HOMEPAGE_ITEMS);

    });

    test('navigate using drawer menu', function() {
        //tap drawer button
        app.findElement(Selector.drawerButton).click();
        app.waitForElement(Selector.drawer);
        assert.isTrue(app.findElement(Selector.drawer).displayed(), Util.TESTLOG_WALKMAN.NAVIGATEUSINGDRAWERMENU_DRAWER_DISPLAYED);

        //show play list view
        app.waitForElement(Selector.drawerPlaylist).tap();
        app.waitForElement(Selector.playlistAdd);
        assert.isTrue(app.findElement(Selector.playlistAdd).displayed(), Util.TESTLOG_WALKMAN.NAVIGATEUSINGDRAWERMENU_PLAYLISTS_ADDBUTTON_DISPLAYED);

        //tap drawer button again
        app.findElement(Selector.drawerButton).click();
        app.waitForElement(Selector.drawer);
        assert.isTrue(app.findElement(Selector.drawer).displayed(), Util.TESTLOG_WALKMAN.NAVIGATEUSINGDRAWERMENU_DRAWER_DISPLAYED_AGAIN);


        //tap walkman menu to show main screen
        app.waitForElement(Selector.drawerHome).tap();
        app.waitForElement(Selector.item);
        assert.isTrue(app.findElements(Selector.item)[0].displayed(), Util.TESTLOG_WALKMAN.NAVIGATEUSINGDRAWERMENU_DRAWER_HOMEPAGE_ITEMS);
    });

});
