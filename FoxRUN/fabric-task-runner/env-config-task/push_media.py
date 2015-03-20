
'''
Instead of the avetest/bin/push-media bash
This script is used for push media content to device
'''

import subprocess
import util_env
from termcolor import colored


def media_push(device = None):

    if device == None:
        device_param = ''
    else:
        device_param = '-s ' + device

    if util_env.MARIONETTE_RUNNER_HOST != 'marionette-firefox-host':
        index = 0
        for webapp_item in util_env.SETPHM_WEBAPPS_LIST:

            if index <= 2 and util_env.APP_NEED_PUSH == ('all' or webapp_item):

                handle_filename_result = subprocess.Popen('adb ' + device_param + ' shell ls ' + util_env.SETPHM_SDCARD + '|grep ' + util_env.SETPHM_WEBAPPS_MEDIAPATH[index], shell=True, stdout=subprocess.PIPE).stdout.read()
                if handle_filename_result == '':
                        subprocess.call('adb root;adb ' + device_param + ' shell mkdir -p ' + util_env.SETPHM_WEBAPPS_MEDIAPATH[index], shell=True)

                handle_value = subprocess.Popen('adb ' + device_param + ' shell ls ' + util_env.SETPHM_WEBAPPS_MEDIAPATH[index] + '|wc -l', shell=True, stdout=subprocess.PIPE).stdout.read()
                if int(handle_value) == 0:
                    subprocess.call('adb ' + device_param + ' push ' + util_env.SETPHM_WEBAPPS_PUSH[index], shell=True)
            index += 1
    else:
        print colored('the util_env.MARIONETTE_RUNNER_HOST = "marionette-firefox-host, stop push"', 'red')