
#This module includes all variables & const definition for pkg : test-exec-task
from fabric.api import *
import subprocess

AVETEST_DIR = subprocess.Popen('(cd ~/avetest;pwd) | tr -d ["\n"]', shell=True, stdout=subprocess.PIPE).stdout.read()
HOME_DIR = subprocess.Popen('(cd ;pwd) | tr -d ["\n"]', shell=True, stdout=subprocess.PIPE).stdout.read()

'''
Vars for Makefile :
'''
LOCAL_DEPLOYMENT_APP_NAME = 'all' # 'album' | 'walkman' | 'movies'
#############################################
#for DEPLOY_OPTIONS:
#'complete' means clone + build + deploy app
#'default' means deploy app
#'terminate' means stop app
DEPLOY_OPTIONS = 'default'  # 'terminate' | 'complete'
#############################################
APP_NEED_PUSH = 'all'
MARIONETTE_RUNNER_HOST_DEVICE = 'marionette-device-host'
MARIONETTE_RUNNER_HOST_FIREFOX = 'marionette-firefox-host'
TEST_MANIFEST = AVETEST_DIR + '/config/test-manifest.json'
REPORTER = 'spec'
TEST_ACCEPTANCE_APP_NAME = [
    'album',
    'walkman',
    'movies'
]
TEST_PERFORMANCE_APP_NAME = [
    'album', #full path is -> /home/CORPUSERS/28851901/avetest/tests/album/performance
    'movies', #full path is -> /home/CORPUSERS/28851901/avetest/tests/movies/performance
    'walkman', #full path is -> /home/CORPUSERS/28851901/avetest/tests/walkman/performance
    'util' #full path is -> /home/CORPUSERS/28851901/avetest/tests/util/performance

]
MOZPERFOUT = 'perfreport'
TEST_ACCEPTANCE_APP_PATH = [
    AVETEST_DIR + '/tests/album/marionette/album_test.js',
    AVETEST_DIR + '/tests/walkman/marionette/walkman_test.js',
    AVETEST_DIR + '/tests/movies/marionette/movies_test.js'
]
ENVCFG_PATH = AVETEST_DIR + '/fabric-task-runner/env-config-task/'
XULRUNNER_BASE_DIRECTORY = AVETEST_DIR + '/xulrunner-sdk-30'
XPCSHELL_PATH = AVETEST_DIR + '/xulrunner-sdk-30/xulrunner-sdk/bin/'

'''
Vars for webdriver_chrome.py :
'''
TESTWEBCHM_WEBDRIVERDEST = AVETEST_DIR + '/smoketest/webdrivertest'


'''
Vars for ave_marionette.py :
'''
TESTAVEM_DEST = AVETEST_DIR + '/smoketest/marionette'


'''
Vars for gaia_perf_marionette.py :
'''
TESTGAIAPERFM_CURRENT_DIR = AVETEST_DIR + '/fabric-task-runner/test-exec-task/'
TESTGAIAPERFM_CONFIG_PATH = AVETEST_DIR + '/config/'  # where all gaia specific customizations for mocha-marionette live.
TESTGAIAPERFM_EXCLUDEAPP = 'util'
TESTGAIAPERFM_GAIA_DIR = AVETEST_DIR
TESTGAIAPERFM_PROFILETEST_PATH = AVETEST_DIR + '/profile-test'


'''
Vars for gaia_marionette.py :
'''
TESTGAIAMARIO_GAIA_DIR = AVETEST_DIR
TESTGAIAMARIO_CONFIG_PATH = TESTGAIAMARIO_GAIA_DIR + '/config/'
TESTGAIAMARIO_NPM_PATH = AVETEST_DIR + '/node_modules'


'''
Vars for setup_python_test.py :
'''
TESTSETPY_TEST_PATH = AVETEST_DIR + '/pythontests/'
TESTSETPY_WEBAPP_TEST = TESTSETPY_TEST_PATH + 'webapptest/'
TESTSETPY_PYENV_PATH = TESTSETPY_TEST_PATH + 'pythonenv'
TESTSETPY_MTBF_PATH = TESTSETPY_TEST_PATH + 'MTBF-Driver'
TESTSETPY_MTBF_URL = 'https://github.com/Mozilla-TWQA/MTBF-Driver.git'
TESTSETPY_B2G_URL = 'https://github.com/mozilla-b2g/B2G.git'
TESTSETPY_B2GPERF_PATH = TESTSETPY_TEST_PATH + 'b2gperf'
TESTSETPY_TEST_TYPE = ['ui', 'endurance', 'mtbf', 'performance', 'b2gperf']

'''
Vars for setup_ave_test.py :
'''
TESTSETAVE_WORKSPACE_ROOT = HOME_DIR + '/.ave'
TESTSETAVE_WORKSPACE_ROOT_CONFIG_JSON = TESTSETAVE_WORKSPACE_ROOT + '/config/workspace.json'
TESTSETAVE_UTILS_ROOT = TESTSETAVE_WORKSPACE_ROOT + '/webapptest'
TESTSETAVE_UTILS_ROOT_BIN = TESTSETAVE_UTILS_ROOT + '/bin'
TESTSETAVE_UTILS_ROOT_PYTEST = TESTSETAVE_UTILS_ROOT + '/pythontests'
TESTSETAVE_CURRENT_PATH = AVETEST_DIR + '/bin'


'''
Vars for run_ave_test.py :
'''
TESTRUNAVE_WORKSPACE_ROOT = HOME_DIR + '/.ave'
TESTRUNAVE_UTILS_ROOT = TESTRUNAVE_WORKSPACE_ROOT + '/webapptest'
