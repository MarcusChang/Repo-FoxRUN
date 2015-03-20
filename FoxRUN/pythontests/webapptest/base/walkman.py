
import time
from marionette.by import By
from app_common import AppCommon

class Walkman(AppCommon):
    name = "Walkman"

    item = (By.CSS_SELECTOR, '.swac-featured .swac-layer img')
    #item = (By.CSS_SELECTOR, '.swac-grid-item .swac-grid-item-content')
    body = (By.CSS_SELECTOR, 'body')
    topBar = (By.CSS_SELECTOR, 'div.swac-top-bar')
    drawerButton = (By.CSS_SELECTOR, 'div.swac-top-bar a.swac-action-nav')
    drawer = (By.CSS_SELECTOR, '.swac-drawer')
    drawerOverlay = (By.CSS_SELECTOR, '.overlay')
    drawerPlaylist = (By.CSS_SELECTOR, '.drawer-playlists')
    drawerWalkman = (By.CSS_SELECTOR, '.drawer-home')
    drawerAlbum = (By.CSS_SELECTOR, '.drawer-albums')
    drawerTracks = (By.CSS_SELECTOR, '.drawer-tracks')
    playlistEdit = (By.CSS_SELECTOR, 'button.icon-edit')
    playlistAdd = (By.CSS_SELECTOR, 'div.toolbar a i.icon-add')
    playlistAddSave = (By.CSS_SELECTOR, 'div.input-addon button.primary-action')
    playlistAddCancel = (By.CSS_SELECTOR, '.main-content .content form.form-group button .icon-delete')
    playlistAddArea = (By.CSS_SELECTOR, '.main-content .content form.form-group')
    playlistSmartList = (By.CSS_SELECTOR, 'ul.track-list')
    playlistUserList = (By.CSS_SELECTOR, 'ul.track-list(2)')
    albumListItem = (By.CSS_SELECTOR, '.sorted-list ul.track-list li a')
    trackListHeader = (By.CSS_SELECTOR, '.main-content .header')
    trackListItem = (By.CSS_SELECTOR, 'div.content ul.track-list li a')
    miniPlayer = (By.CSS_SELECTOR, '.miniplayer')
    miniPlayerPlay = (By.CSS_SELECTOR, '.miniplayer .icon-musiccontrol_play')
    miniPlayerPause = (By.CSS_SELECTOR, '.miniplayer .icon-musiccontrol_pause')

    def setUp(self):
        self.push_media(self.name,self.marionette.device_serial)

    def show_drawer(self):
        self.wait_for_element_displayed(*self.drawerButton)
        self.marionette.find_element(*self.drawerButton).tap()
        self.wait_for_element_displayed(*self.drawer)
        return self.is_element_displayed(*self.drawer)

    def show_tracklist(self):
        #show album list view
        self.wait_for_element_displayed(*self.drawerTracks)
        time.sleep(self.wait_short)
        self.marionette.find_element(*self.drawerTracks).tap()
        self.wait_for_element_displayed(*self.trackListItem)
        return self.is_elements_displayed(*self.trackListItem)

    def press_tracklist(self):
        #press a track list and play 2 seconds
        self.marionette.find_element(*self.trackListItem).tap()
        self.wait_for_element_displayed(*self.miniPlayerPause)
        return self.is_element_displayed(*self.miniPlayerPause)

    def press_pause(self):
        #press pause button
        self.marionette.find_element(*self.miniPlayerPause).tap()
        self.wait_for_element_displayed(*self.miniPlayerPlay)
        return self.is_element_displayed(*self.miniPlayerPlay)

    def show_mainview(self):
        #tap walkman menu to show main screen
        self.wait_for_element_displayed(*self.drawerWalkman)
        time.sleep(self.wait_short)
        self.marionette.find_element(*self.drawerWalkman).tap()
        self.wait_for_element_displayed(*self.item)
        return self.is_elements_displayed(*self.item)

    def show_playlist(self):
        #tap walkman menu to show main screen
        self.wait_for_element_displayed(*self.drawerPlaylist)
        time.sleep(self.wait_short)
        self.marionette.find_element(*self.drawerPlaylist).tap()
        self.wait_for_element_displayed(*self.playlistAdd)
        return self.is_element_displayed(*self.playlistAdd)

    def scroll_mainview(self):
        y1 = self.marionette.find_element(*self.topBar).location['y']
        self._flick("next",self.name)
        y2 = self.marionette.find_element(*self.topBar).location['y']
        self._flick("up",self.name)
        return (y1, y2)


