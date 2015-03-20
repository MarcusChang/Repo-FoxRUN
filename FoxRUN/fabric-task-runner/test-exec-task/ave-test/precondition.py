__author__ = 'Jay (XP016283)'

'''
Instead of the avetest/bin/config-init.sh
This script is used for adding the parmater from user input into config file, "manifest.ini" and "mtbf.list","ApplicationList.ini"
'''

import subprocess
import util_ave


def precondition(device='BL4823D06303'):
    workspace_root = util_ave.HOME_DIR+'/.ave'
    utils_root = workspace_root+'/webapptest'
    subprocess.call('pushd ' + utils_root + ' > /dev/null', shell=True)
    print ('pushd ' + utils_root + ' > /dev/null')
    subprocess.call('cd ~/avetest/;make precondition device=' + device, shell=True)
    print('cdmake precondition device=' + device)
    # subprocess.call('popd > /dev/null', shell=True)


def main():
    precondition()

main()









