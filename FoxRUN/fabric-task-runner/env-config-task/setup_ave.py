
'''
Instead of the avetest/bin/setup-ave bash
This script is used for setup AVE Marionette
'''


import subprocess
import util_env

def ave_setup():

    print('we are going to install AVE')
    handleDpkgAve = subprocess.Popen('dpkg -s ave | grep Status', shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    if (handleDpkgAve != util_env.SETAVE_INSTALLED_OK):
        print('-------------Updating the list of available packages---------')
        subprocess.call('sudo apt-get update', shell=True)
        print('Downloading ave...')
        subprocess.call('sudo apt-get install ave', shell=True)
    else:
        handleAveVersionShow = subprocess.Popen('apt-cache show ave | grep Version | head -1', shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
        handleDpkgAveVersion = subprocess.Popen('dpkg -s ave | grep Version', shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
        if (handleAveVersionShow != handleDpkgAveVersion):
            print('New package be available for installation')
            print('Updating the list of available packages')
            subprocess.call('sudo apt-get update', shell=True)
            print('Downloading ave...')
            subprocess.call('sudo apt-get install ave', shell=True)
        else:
            print('latest ave is already installed')