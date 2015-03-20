
'''
Instead of the avetest/bin/gaia-marionette bash
This script is used for run the acceptance test.
'''

import os
import util_test
import subprocess
import sys
sys.path.append(util_test.ENVCFG_PATH)
import setup_xulrunner
import push_media
import setup_platform

from termcolor import colored



def marionette_gaia(appname, testJob, m_host = 'device'):
    global script_gaia
    global host_gaia
    manifest_gaia = util_test.TEST_MANIFEST
    reporter_gaia = util_test.REPORTER
    if m_host == 'device':
        host_gaia = util_test.MARIONETTE_RUNNER_HOST_DEVICE
    elif m_host == 'firefox':
        host_gaia = util_test.MARIONETTE_RUNNER_HOST_FIREFOX
        subprocess.call('firefox --marionette', shell=True)
    if testJob == 'test-acceptance':
        setup_xulrunner.xulrunner_setup()
        push_media.media_push()
        script_gaia = util_test.TESTGAIAMARIO_GAIA_DIR + '/tests/' + appname + '/marionette/' + appname + '_test.js'
    if testJob == 'test-platform':
        setup_xulrunner.xulrunner_setup()
        setup_platform.platform_setup()
        script_gaia = util_test.TESTGAIAMARIO_GAIA_DIR + '/tests/' + appname + '/platform/' + appname + '_test.js'
    # make sure node_modules are installed
    if not os.path.exists(util_test.TESTGAIAMARIO_NPM_PATH):
        subprocess.call('(cd ' + util_test.TESTGAIAMARIO_GAIA_DIR + ' && npm install)', shell=True)
        handle_npm_modules = subprocess.Popen('ls -d "' + util_test.TESTGAIAMARIO_GAIA_DIR + '/node"*', shell=True, stdout=subprocess.PIPE).stdout.read()
    if not os.path.exists(util_test.XULRUNNER_BASE_DIRECTORY):
        print colored('handle_xulrunner_dir will begin', 'red')
        # the xulrunner directory isn't in the environment
        handle_xulrunner_dir = subprocess.Popen('ls -d "' + util_test.TESTGAIAMARIO_GAIA_DIR + '/xulrunner-sdk"*/xulrunner-sdk | sort -nr', shell=True, stdout=subprocess.PIPE).stdout.read()
        if handle_xulrunner_dir == None:
            print colored("Couldn't find XULrunner. Please execute this file from 'make' or install XULrunner yourself.", 'red')

    # wrap marionette-mocha with gaia's defaults. We also need to alter the paths to
    # xpcshell in available for email fake servers.
    subprocess.call('PATH=' + util_test.XPCSHELL_PATH + ':' + '$PATH' + ' ' + util_test.TESTGAIAMARIO_GAIA_DIR + '/node_modules/.bin/marionette-mocha ' + '--timeout 20s --ui tdd ' + util_test.TESTGAIAMARIO_CONFIG_PATH + 'setup.js ' + script_gaia + ' --host ' + host_gaia + ' --manifest ' + manifest_gaia + ' --reporter ' + reporter_gaia, shell=True)