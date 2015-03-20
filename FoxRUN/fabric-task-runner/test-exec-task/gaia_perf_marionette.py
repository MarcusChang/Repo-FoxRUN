
'''
Instead of the avetest/bin/gaia-perf-marionette bash
This script is used for prepare the performance test environment.
'''

import os
import util_test
import subprocess
from termcolor import colored

def test_perf(App, perfTime):

# make sure node_modules are 100% up to date
    subprocess.call('make node_modules', shell=True)

    if util_test.MARIONETTE_RUNNER_HOST_DEVICE == 'marionette-b2gdesktop-host':
        # download b2g-desktop (if its not present)
        subprocess.call('make -C ' + util_test.TESTGAIAPERFM_GAIA_DIR + ' b2g', shell=True)
    # tests can timeout without the profile-test folder so build it here.
    if not os.path.exists(util_test.TESTGAIAPERFM_PROFILETEST_PATH):
        subprocess.call('profile-test make -C ' + util_test.TESTGAIAPERFM_GAIA_DIR, shell=True)
    if not os.path.exists(util_test.XULRUNNER_BASE_DIRECTORY):
        # the xulrunner directory isn't in the environment
        handle_xulrunner_directory = subprocess.Popen('ls -d "' + util_test.TESTGAIAPERFM_GAIA_DIR + '/../xulrunner-sdk"*/xulrunner-sdk | sort -nr | head -n1 2> /dev/null', shell=True, stdout=subprocess.PIPE).stdout.read()
        if handle_xulrunner_directory == None:
            print colored("Couldn't find XULrunner. Please execute this file from 'make' or install XULrunner yourself.", 'red')
    if App == None:
        print colored("APPS isn't defined. Cannot continue.", 'red')
    elif App == util_test.TEST_PERFORMANCE_APP_NAME[0]:
        print('the target App = ' + util_test.TEST_PERFORMANCE_APP_NAME[0])
    elif App == util_test.TEST_PERFORMANCE_APP_NAME[1]:
        print('the target App = ' + util_test.TEST_PERFORMANCE_APP_NAME[1])
    elif App == util_test.TEST_PERFORMANCE_APP_NAME[2]:
        print('the target App = ' + util_test.TEST_PERFORMANCE_APP_NAME[2])
    elif App == util_test.TEST_PERFORMANCE_APP_NAME[3]:
        print('the target App = ' + util_test.TEST_PERFORMANCE_APP_NAME[3])

    subprocess.call("echo '[' >&3", shell=True)
    handle_shared_perf = subprocess.Popen('find ' + util_test.TESTGAIAPERFM_GAIA_DIR + 'tests/util/performance -name "*_test.js" -type f', shell=True, stdout=subprocess.PIPE).stdout.read()
    handle_files_perf = subprocess.Popen('test -d ' + util_test.TESTGAIAPERFM_GAIA_DIR + 'tests/' + App + '/performance && find ' + util_test.TESTGAIAPERFM_GAIA_DIR + 'tests/' + App + '/performance -name "*_test.js" -type f', shell=True, stdout=subprocess.PIPE).stdout.read()
    # wrap marionette-mocha with gaia's defaults. We also need to alter the paths to
    # xpcshell in available for email fake servers.
    if App != util_test.TESTGAIAPERFM_EXCLUDEAPP:
        subprocess.call('export CURRENT_APP=' + App, shell=True)
        subprocess.call('PATH=' + util_test.XPCSHELL_PATH + ':' + '$PATH' + ' ' + util_test.TESTGAIAPERFM_GAIA_DIR + 'node_modules/.bin/marionette-mocha ' + '--timeout ' + perfTime + 's --ui tdd --host ' + util_test.MARIONETTE_RUNNER_HOST_DEVICE + ' ' + util_test.TESTGAIAPERFM_CONFIG_PATH + 'setup.js ' + util_test.TESTGAIAPERFM_GAIA_DIR + 'test/util/performance/perf.js ' + handle_shared_perf + ' ' + handle_files_perf + ' -R ' + util_test.TESTGAIAPERFM_GAIA_DIR + 'tests/util/performance/jsonmozperf.js ' + '$@ >&3', shell=True)
    subprocess.call("echo ']' >&3", shell=True)




