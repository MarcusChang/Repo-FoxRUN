
'''
Instead of the avetest/bin/webdriver-chrome bash
This script is used for run JAVA WebDriver test.
'''

import util_test
import subprocess
import sys
sys.path.append(util_test.ENVCFG_PATH)
import setup_chromedriver


def webdriver_chrome_test():

# install the chrome driver first

    setup_chromedriver.chromedriver_setup()
    print('webdriver_chrome started...')
    subprocess.call('pushd ' + util_test.TESTWEBCHM_WEBDRIVERDEST + ' > /dev/null', shell=True)
    subprocess.call('ant run', shell=True)
    subprocess.call('popd > /dev/null', shell=True)

