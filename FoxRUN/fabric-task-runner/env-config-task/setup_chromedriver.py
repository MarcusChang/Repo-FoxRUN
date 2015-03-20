
'''
Instead of the avetest/bin/setup-chromedriver bash
This script is used for setup webdriver/chromedriver
'''

import os
import subprocess
import util_env

def chromedriver_setup():

    print('we are going to install chromedriver')
    if not os.path.exists(util_env.SETCHM_CHROMEDRIVER_PATH):
        print('Downloading chromedriver...')
        handle_dest = subprocess.Popen('mktemp -d', shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
        print('handle_dest---------------------->'+handle_dest)

        subprocess.call('pushd ' + handle_dest + ' > /dev/null ;' + \
                        'wget -O chromedriver.zip ' + util_env.SETCHM_PKG +\
                        '; unzip chromedriver.zip ' +\
                        '; chmod +x chromedriver' +\
                        '; popd > /dev/null'
                        , shell=True)
        subprocess.call('cp ' + handle_dest +'/chromedriver' + ' ' + util_env.HOME_DIR+'/avetest_1113.bak/smoketest/webdrivertest/chromedriver', shell=True)
        subprocess.call('rm -r ' + handle_dest, shell=True)
    else:
        print('chromedriver is already installed')








