
'''
Instead of the avetest/bin/ave-marionette bash
This script is used for run the smoketest/marionettetest scripts.
'''


import util_test
import subprocess
import sys
sys.path.append(util_test.ENVCFG_PATH)
import setup_ave

def ave_marionette_test():

# install the ave environment first
    setup_ave.ave_setup()
# run JS Marionette Test
    print('ave-marionette started')
    subprocess.call('pushd ' + util_test.TESTAVEM_DEST + ' > /dev/null', shell=True)
    subprocess.call('ave-broker --restart', shell=True)
    subprocess.call('vcsjob execute -j. -t ave-marionette-test', shell=True)
    subprocess.call('popd > /dev/null', shell=True)
