
'''
Instead of the avetest/bin/setup-platform bash
This script is used for download isolate app for test.
For phone, need to install app by firerfox app manager. For browser, directly use dowloaded file.
Use git clone due to wget need to input username and password in command line
'''

import os
import subprocess
import util_env
import time

def platform_setup():

    if not os.path.exists(util_env.SETPLT_ROOTDIR):
        subprocess.call('mkdir ' + util_env.SETPLT_ROOTDIR, shell=True)

    subprocess.call('adb forward tcp:6000 localfilesystem:/data/local/debugger-socket', shell=True)
    subprocess.call('pushd ' + util_env.SETPLT_ROOTDIR + ' > /dev/null', shell=True)
    index = 0
    for isolate_app in util_env.SETPLT_ISOLATE_APPS_LIST:
        if (util_env.LOCAL_DEPLOYMENT_APP_NAME == 'all'):
            if not os.path.exists(util_env.SETPLT_ROOTDIR + '/' + isolate_app):
                handleIsolateIndex = subprocess.Popen('git clone ' + util_env.SETPLT_ISOLATE_APPS_URL[index], shell=True, stdout=subprocess.PIPE).stdout.read()
                if not handleIsolateIndex:
                    index += 1
            else:
                subprocess.call('pushd ' + util_env.SETPLT_ROOTDIR + ' > /dev/null', shell=True)
                subprocess.call('git pull', shell=True)
                subprocess.call('popd > /dev/null', shell=True)
            ID = subprocess.Popen('echo ' + isolate_app + ' | tr A-Z a-z', shell=True, stdout=subprocess.PIPE).stdout.read()
            print('PUSHING *' + ID + '* as packaged app')
            subprocess.call('adb push ' + util_env.SETPLT_ROOTDIR + '/isolate_app/application.zip' + ' /data/local/tmp/b2g/' + ID + '/application.zip', shell=True)
            print('!!! CONFIRM THE PROMPT on the phone !!!')
            LD_LIBRARY_PATH = util_env.SETPLT_XPCSHELL_LIBRARY_PATH + ' ' + util_env.SETPLT_XPCSHELL + ' ' + util_env.SETPLT_JS + ' ' + ID + ' ' + '6000'
            time.sleep(10)
            subprocess.call('popd > /dev/null', shell=True)
        index += 1
    subprocess.call('popd > /dev/null', shell=True)





