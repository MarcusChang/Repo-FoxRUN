
'''
Instead of the avetest/bin/setup-xulrunner bash
This script is used for setup the firefox xulrunner (xpcshell)
'''

import os
import subprocess
import util_env

def xulrunner_setup():

    print('setup xulrunner configuring...')
    subprocess.call(util_env.SETXUL_EXPORT_XULD_XULR_XPC, shell=True)
    subprocess.call(util_env.SETXUL_ECHO_XUL_PATH, shell=True)
    if not os.path.exists(util_env.SETXUL_XULRUNNER_BASE_DIRECTORY):
        print('Downloading XULRunner...')
        subprocess.call('wget -c ' + util_env.SETXUL_XULRUNNER_SDK_DOWNLOAD, shell=True)
        subprocess.call('mkdir ' + util_env.SETXUL_XULRUNNER_BASE_DIRECTORY, shell=True)
        print('Unzipping XULRunner...')
        subprocess.call('tar xjf xulrunner*.tar.bz2 -C ' + util_env.SETXUL_XULRUNNER_BASE_DIRECTORY, shell=True)
        print('Removing XULRunner tar package...')
        subprocess.call('rm -f xulrunner*.tar.bz2', shell=True)
        subprocess.call('echo ' + util_env.SETXUL_XULRUNNER_SDK_DOWNLOAD + ' > ' +util_env.SETXUL_XULRUNNER_URL_FILE, shell=True)
    else:
        handleXulSdkDwn = subprocess.Popen('cat ' + util_env.SETXUL_XULRUNNER_URL_FILE, shell=True, stdout=subprocess.PIPE).stdout.read()
        handleXulSdkDwn_url=handleXulSdkDwn[:-1]
        print ('Util url----------->'+util_env.SETXUL_XULRUNNER_SDK_DOWNLOAD)
        print ('File url----------->'+handleXulSdkDwn_url)
        if (util_env.SETXUL_XULRUNNER_SDK_DOWNLOAD != handleXulSdkDwn_url):
            print('XULRunner version is not correct')
            subprocess.call('rm -rf ' + util_env.SETXUL_XULRUNNER_BASE_DIRECTORY, shell=True)
            subprocess.call('mkdir ' + util_env.SETXUL_XULRUNNER_BASE_DIRECTORY, shell=True)
            print('Downloading XULRunner...')
            subprocess.call('wget -c ' + util_env.SETXUL_XULRUNNER_SDK_DOWNLOAD, shell=True)
            print('Unzipping XULRunner...')
            subprocess.call('tar xjf xulrunner*.tar.bz2 -C ' + util_env.SETXUL_XULRUNNER_BASE_DIRECTORY, shell=True)
            print('Removing XULRunner tar pacakge...')
            subprocess.call('rm -f xulrunner*.tar.bz2', shell=True)
            subprocess.call('echo ' + util_env.SETXUL_XULRUNNER_SDK_DOWNLOAD + ' > ' +util_env.SETXUL_XULRUNNER_URL_FILE, shell=True)
        else:
            print('XULRunner is installed already')





