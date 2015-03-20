
'''
Instead of the avetest/bin/setup-forward-devices bash
This script is to modfiy marionette.py so that it can support multiple devices test on one PC
'''

import os
import subprocess
import util_env
from termcolor import colored

def forward_devices_setup():
    if os.path.exists(util_env.SETFWD_MARIONETTE_PATH_FILE):
        open_marionette_file = open(util_env.SETFWD_MARIONETTE_PATH_FILE, 'rw')
        for line in open_marionette_file.readlines():
            if line == util_env.SETFWD_STRSYS:
                subprocess.call('sed -i '+'s/ ' + util_env.SETFWD_STRSESSION + '/& ' + str('\\n') + util_env.SETFWD_CONDTION + util_env.SETFWD_FORWARD + '/" ' + line, shell=True)
            else:
                print colored('line not changed', 'red')
    else:
        print colored('file not exit', 'red')






