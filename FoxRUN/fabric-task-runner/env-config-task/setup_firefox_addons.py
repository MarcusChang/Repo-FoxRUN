
'''
Instead of the avetest/bin/setup-firefox-addons bash
This script is used for setup the firefox addons
'''

import os
import subprocess
import util_env
from termcolor import colored

def firefox_addons_setup():

    if not os.path.exists(util_env.SETFFA_FFPATH):
        print('please install firefox browser firstly')
        subprocess.call('exit 1', shell=True)
    else:
        handle_FIREFOX_EXTENSION_PATH = subprocess.Popen('cat ~/.mozilla/firefox/profiles.ini | grep Path ', shell=True, stdout=subprocess.PIPE).stdout.read()
        handle_FIREFOX_EXTENSION_PATH_TRUNCATE = subprocess.Popen('echo ' + handle_FIREFOX_EXTENSION_PATH + ' | cut -c6-', shell=True, stdout=subprocess.PIPE).stdout.read()
        fireFoxAddonAdapter_Path = '~/.mozilla/firefox/' + handle_FIREFOX_EXTENSION_PATH_TRUNCATE + '/extensions/' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER
        if not os.path.exists(fireFoxAddonAdapter_Path):
            subprocess.call('mkdir ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER, shell=True)
            subprocess.call('pushd ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER + ' > /dev/null', shell=True)
            #install firefox addons adbhelper
            print('we are going to download adbhelper...')
            subprocess.call('wget -c ' + util_env.SETFFA_ADBHELPER_URL, shell=True)
            subprocess.call('popd > /dev/null', shell=True)
            adbhelper_xpi_path = '~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER + '/adbhelper-linux64-latest.xpi'
            if not os.path.exists(adbhelper_xpi_path):
                print colored('FATAL error: can NOT download adbhelper-linux64-latest.xpi', 'red')
            else:
                print('we are going to install adbhelper@mozilla.org')
                subprocess.call('cp ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER + '/adbhelper-linux64-latest.xpi ./', shell=True)
                subprocess.call('rm ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER + '/ -rf', shell=True)
                subprocess.call('gnome-terminal -x firefox adbhelper-linux64-latest.xpi', shell=True)
                subprocess.call('unzip adbhelper-linux64-latest.xpi', shell=True)
                subprocess.call('cp ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER + ' ~/.mozilla/firefox/' + handle_FIREFOX_EXTENSION_PATH_TRUNCATE + '/extensions/ -r', shell=True)
                subprocess.call('rm ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER + ' -rf', shell=True)
                subprocess.call('gnome-terminal -x firefox -url about:newaddon?id=' + util_env.SETFFA_FIREFOX_ADDONS_ABDHELPER, shell=True)
        firefoxExtensionsPath = '~/.mozilla/firefox/' + handle_FIREFOX_EXTENSION_PATH_TRUNCATE + '/extensions/' + util_env.SETFFA_FIREFOX_ADDONS_FXOSSIMULATOR
        if not os.path.exists(firefoxExtensionsPath):
            subprocess.call('mkdir ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_FXOSSIMULATOR, shell=True)
            subprocess.call('pushd ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_FXOSSIMULATOR + ' > /dev/null', shell=True)
            #install firefox addons fxos simulator
            print('we are going to download fxos simulator')
            subprocess.call('wget -c ' + util_env.SETFFA_FXOS_SIMULATOR_URL, shell=True)
            subprocess.call('popd > /dev/null', shell=True)
            if not os.path.exists(util_env.SETFFA_FXOS_SIMULATOR_PATH):
                print colored('FATAL error: can NOT download fxos_1_2_simulator-linux64-latest.xpi', 'red')
            else:
                print('we are going to install fxos_1_2_simulator@mozilla.org')
                subprocess.call('cp ' + util_env.SETFFA_FXOS_SIMULATOR_PATH + ' ./', shell=True)
                subprocess.call('rm ~/tmp/' + util_env.SETFFA_FIREFOX_ADDONS_FXOSSIMULATOR + '/ -rf', shell=True)
                subprocess.call('gnome-terminal -x firefox fxos_1_2_simulator-linux64-latest.xpi', shell=True)






















