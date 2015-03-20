
'''
Instead of the avetest/bin/setup-gaiatest-env bash
This script is used for setup the gaiatest env
'''

import os
import subprocess
import util_env
from termcolor import colored
import sys


def setup_gaiatest_env():
    #download test content
    if not os.path.exists(util_env.AVETEST_DIR + '/test_media'):
        handle_version = subprocess.Popen('repository listrevisions fxrun-ave-testmedia -pc testcontent | tail -1', shell=True, stdout=subprocess.PIPE).stdout.read()
        handle_name = subprocess.Popen('fxrun-ave-testmedia_'+handle_version+'_all.deb', shell=True, stdout=subprocess.PIPE).stdout.read()
        subprocess.call('repository getpackage -pc testcontent fxrun-ave-testmedia '+handle_version, shell=True)
        subprocess.call('dpkg -x '+handle_name, shell=True)
        subprocess.call('rm '+handle_name, shell=True)
        # os.remove(handle_name)

    #MTBF env setup. clone gaia and mtbf-driver.
    handle_virtualenv = subprocess.Popen('which virtualenv', shell=True, stdout=subprocess.PIPE).stdout.read()
    if not os.path.isfile(handle_virtualenv):
        subprocess.call('sudo apt-get install python-virtualenv', shell=True)
        handle_virtualenv = subprocess.Popen('which virtualenv', shell=True, stdout=subprocess.PIPE).stdout.read()

    if not os.path.exists(util_env.TEST_SETGAIA_PATH + '/pythonenv'):
        subprocess.call('pushd '+util_env.TEST_SETGAIA_PATH +' > /dev/null;'\
                        +handle_virtualenv+' pythonenv;'\
                        +'popd > /dev/null', shell=True)

    # subprocess.call('source '+util_env.TEST_SETGAIA_PATH+'/pythonenv/bin/activate', shell=True)

    if not os.path.exists(util_env.TEST_SETGAIA_PATH+'/MTBF-Driver'):
        subprocess.call('source '+util_env.TEST_SETGAIA_PATH+'/pythonenv/bin/activate;'\
                        'pushd '+util_env.TEST_SETGAIA_PATH+' > /dev/null;'\
                        'git clone https://github.com/Mozilla-TWQA/MTBF-Driver.git;'\
                        'git clone https://github.com/mozilla-b2g/B2G.git;'\
                        'cp -r '+util_env.TEST_SETGAIA_PATH + '/B2G/tools '+util_env.TEST_SETGAIA_PATH +'/MTBF-Driver/mtbf_driver;'\
                        'touch '+util_env.TEST_SETGAIA_PATH +'/MTBF-Driver/mtbf_driver/tools/__init__.py;'\
                        'rm -rf B2G;'\
                        'popd > /dev/null;'\
                        'pushd '+util_env.TEST_SETGAIA_PATH+'/MTBF-Driver > /dev/null;'\
                        'python setup.py develop;'\
                        'popd > /dev/null', shell=True)
    else:
        subprocess.call('source '+util_env.TEST_SETGAIA_PATH+'/pythonenv/bin/activate;'\
                        'pushd '+util_env.TEST_SETGAIA_PATH+'/MTBF-Driver > /dev/null;'\
                        'git pull;'\
                        'python setup.py develop;'\
                        'popd > /dev/null', shell=True)

    subprocess.call('source '+util_env.TEST_SETGAIA_PATH+'/pythonenv/bin/activate;'\
                    'pushd '+util_env.TEST_SETGAIA_PATH+' > /dev/null;'\
                    'python setup.py develop;'\
                    'popd > /dev/null',shell=True)

    if not os.path.exists(util_env.TEST_SETGAIA_PATH+'/pythonenv/lib/python2.7/site-packages/b2gperf'):
        subprocess.call('source '+util_env.TEST_SETGAIA_PATH+'/pythonenv/bin/activate;'\
                        'pip install b2gperf', shell=True)





