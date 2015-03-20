
#This module includes all variables & const definition for pkg : env-config-task

from fabric.api import *
import subprocess

HOME_DIR = subprocess.Popen('(cd ;pwd) | tr -d ["\n"]', shell=True, stdout=subprocess.PIPE).stdout.read()
AVETEST_DIR = subprocess.Popen('(cd ' + HOME_DIR + '/avetest;pwd) | tr -d ["\n"]', shell=True, stdout=subprocess.PIPE).stdout.read()

'''
Vars for Makefile :
'''
LOCAL_DEPLOYMENT_APP_NAME = 'all' # 'album' | 'walkman' | 'movies'
#############################################
#for DEPLOY_OPTIONS:
#'complete' means clone + build + deploy app
#'default' means deploy app
#'terminate' means stop app
DEPLOY_OPTIONS = 'default' # 'terminate' | 'complete'
#############################################
APP_NEED_PUSH = 'all'
MARIONETTE_RUNNER_HOST = 'marionette-device-host'
#MARIONETTE_RUNNER_HOST = 'marionette-firefox-host'


'''
Vars for setup_xulrunner.py :
'''
SETXUL_XULRUNNER_BASE_DIRECTORY = AVETEST_DIR + '/xulrunner-sdk-30'
SETXUL_XULRUNNER_DIRECTORY = SETXUL_XULRUNNER_BASE_DIRECTORY + '/xulrunner-sdk'
SETXUL_XULRUNNER_URL_FILE = SETXUL_XULRUNNER_BASE_DIRECTORY +'/.url'
SETXUL_XULRUNNER_SDK_DOWNLOAD = 'http://ftp.mozilla.org/pub/mozilla.org/xulrunner/nightly/2014/03/2014-03-08-03-02-03-mozilla-central/xulrunner-30.0a1.en-US.linux-x86_64.sdk.tar.bz2'
SETXUL_XULRUNNERSDK = SETXUL_XULRUNNER_DIRECTORY + '/bin/run-mozilla.sh'
SETXUL_XPCSHELLSDK = SETXUL_XULRUNNER_DIRECTORY + '/bin/xpcshell'
SETXUL_EXPORT_XULD_XULR_XPC = 'export XULRUNNER_DIRECTORY XULRUNNERSDK XPCSHELLSDK'
SETXUL_ECHO_XUL_PATH = "echo XULrunner directory: " + SETXUL_XULRUNNER_DIRECTORY

'''
Vars for setup_ave.py :
'''
SETAVE_INSTALLED_OK = 'Status: install ok installed'


'''
Vars for setup_platform.py :
'''
SETPLT_XULRUNNER_DIRECTORY = AVETEST_DIR + '/xulrunner-sdk-30/xulrunner-sdk'
SETPLT_XPCSHELL = SETPLT_XULRUNNER_DIRECTORY + '/bin/xpcshell'
SETPLT_XPCSHELL_LIBRARY_PATH = SETPLT_XULRUNNER_DIRECTORY + '/bin:' + SETPLT_XULRUNNER_DIRECTORY + '/lib'
SETPLT_JS = AVETEST_DIR + '/fabric-task-runner/env-config-task/install-app.js'
SETPLT_ROOTDIR = AVETEST_DIR + '/platform_apps'
SETPLT_FLIP = 'flipping-tiles'
SETPLT_INFINITE = 'infinite-scroll'
SETPLT_TRANSITION = 'transitions-performance'
SETPLT_URL_PREFIX = 'git@code.marcus_chang.com:platform-issues'
SETPLT_ISOLATE_APPS_LIST = [SETPLT_FLIP, SETPLT_INFINITE, SETPLT_TRANSITION]
SETPLT_ISOLATE_APPS_URL = [
    SETPLT_URL_PREFIX + '/' + SETPLT_FLIP + '.git',
    SETPLT_URL_PREFIX + '/' + SETPLT_INFINITE + '.git',
    SETPLT_URL_PREFIX + '/' + SETPLT_TRANSITION + '.git'
]
SETPLT_INDEX = 0


'''
Vars for setup_chromedriver.py :
'''
SETCHM_CHROMEDRIVER_PATH = AVETEST_DIR + '/smoketest/webdrivertest/chromedriver'
SETCHM_PKG = 'http://nb.baidupcs.com/file/e76c1a3e4b1fc70042972ef0b2679dae?bkt=p2-nb-436&fid=1561077172-250528-243513569173458&time=1415955176&sign=FDTAXERB-DCb740ccc5511e5e8fedcff06b081203-RKF7%2BwXBoY4VwBpdV5dIMReNsUo%3D&to=nbb&fm=Nin,B,T,t&newver=1&newfm=1&flow_ver=3&expires=8h&rt=pr&r=486084127&mlogid=859094273&vuk=1561077172&vbdid=1425445472&fin=FFMOVIES-2.zip'
SETCHM_DEST = 'mktemp -d'


'''
Vars for setup_firefox_addons.py :
'''
SETFFA_FFPATH = '~/.mozilla/firefox'
SETFFA_FIREFOX_ADDONS_ABDHELPER = 'adbhelper@mozilla.org'
SETFFA_FIREFOX_ADDONS_FXOSSIMULATOR = 'fxos_1_2_simulator@mozilla.org'
SETFFA_ADBHELPER_URL = 'https://ftp.mozilla.org/pub/mozilla.org/labs/fxos-simulator/adb-helper/linux64/adbhelper-linux64-latest.xpi'
SETFFA_FXOS_SIMULATOR_URL = 'https://ftp.mozilla.org/pub/mozilla.org/labs/fxos-simulator/1.2/linux64/fxos_1_2_simulator-linux64-latest.xpi'
SETFFA_FXOS_SIMULATOR_PATH = '~/tmp/' + SETFFA_FIREFOX_ADDONS_FXOSSIMULATOR + '/fxos_1_2_simulator-linux64-latest.xpi'


'''
Vars for app_deploy.py :
'''
SETAPD_NOTHING_TO_COMMIT="nothing to commit, working directory clean"
SETAPD_WEBAPPS_LIST = [
    'album',
    'movies',
    'walkman'
]
SETAPD_WEBAPPS_PORT = [
    8485,
    8486,
    8487,
    8488
]
SETAPD_NODE = 'which node'
SETAPD_BASE_WORKING_DIRECTORY = AVETEST_DIR + '/webapps/'
SETAPD_BASE_WORKING_DIRECTORY_LOGS = AVETEST_DIR + '/webapps/logs/'
SETAPD_BASE_WORKING_DIRECTORY_PIDS = AVETEST_DIR + '/webapps/pids/'


'''
Vars for push_media.py :
'''
SETPHM_WEBAPPS_LIST = [
    'album',
    'movies',
    'walkman'
]

SETPHM_SDCARD = '/sdcard1/'

SETPHM_WEBAPPS_PUSH = [
    AVETEST_DIR + '/test_media/DCIM ' + SETPHM_SDCARD + 'DCIM',
    AVETEST_DIR + '/test_media/Movies ' + SETPHM_SDCARD + 'Movies',
    AVETEST_DIR + '/test_media/Music ' + SETPHM_SDCARD + 'Music'
]

SETPHM_WEBAPPS_MEDIAPATH = [
    SETPHM_SDCARD + 'DCIM',
    SETPHM_SDCARD + 'Movies',
    SETPHM_SDCARD + 'Music'
]

'''
Vars for setup_forward_devices.py :
'''

SETFWD_MARIONETTE_PATH_FILE = AVETEST_DIR+"/pythontests/pythonenv/marionette.py"
SETFWD_STRSESSION = "start_session(self, desired_capabilities=None):"
SETFWD_STRSYS = "os.system"
SETFWD_CONDTION = "        if (self.device_serial != None):\n"
SETFWD_FORWARD = "             os.system(\"adb -s \"+self.device_serial+\" forward tcp:2828 tcp:2828\")\n"


'''
Vars for setup_gaiatest_env.py :
'''
TEST_SETGAIA_PATH = AVETEST_DIR + '/pythontests'
TEST_SETGAIA_WEBAPP = TEST_SETGAIA_PATH + '/webapptest'




