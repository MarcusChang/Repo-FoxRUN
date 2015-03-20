__author__ = 'Jay (XP016283)'

'''
Instead of the avetest/bin/ave-test/download-rom bash
This script is used for run the ave based mtbf, ui, endurance and performance test.
'''

import os
import util_test
import subprocess
from termcolor import colored
import sys
sys.path.append(util_test.ENVCFG_PATH)
import shutil
#import zipfile


workspace_root = util_test.HOME_DIR +'/.ave'
uitls_root = workspace_root + '/webapptest'
subprocess.call('pushd ' + uitls_root +'/bin/ave-test > /dev/null', shell=True)
devices = [
    'proto_t',
    'proto_f',
    'ff1'
]
artifacts = [
    'daily_build_ffos',
    'daily_build_kk-helenium-pre-v2.1',
    'daily_build_kk-helenium-pre-v2.1'
]
device_names = [
    'proto_t',
    'ff1 ',
    'ff1'
]

def download_rom(device = None):
    global device_param
    if device == None:
        device_param = ''
    else:
        device_param = '-s' + device

# currently ro.product.model ro.product.name ro.product.device are same. Such as "proto_t", "proto_f"
# $device has a ^M character.
device = subprocess.Popen('adb ' + device_param + 'shell getprop ro.product.model', shell=True, stdout=subprocess.PIPE).stdout.read()
device = subprocess.Popen('${' + device + ':0:' + '$((${#' + device + '}-1))', shell=True, stdout=subprocess.PIPE).stdout.read()
serialno = subprocess.Popen('adb ' + device_param + 'shell getprop ro.serialno', shell=True, stdout=subprocess.PIPE).stdout.read()
serialno = subprocess.Popen('${' + serialno + ':0:' + '$((${#' + serialno + '}-1))', shell=True, stdout=subprocess.PIPE).stdout.read()
artifact = ""
for i in devices:
    if device == i:
        artifact = artifacts[i]
        device_name = device_names[i]

# Get the package name to be flashed
subprocess.call('wget --no-proxy --output-document=' + device +'.json http://android-ci-platform.marcus_chang.com/job/$artifact/lastSuccessfulBuild/api/json?pretty=true', shell=True)
line = subprocess.Popen('cat' +device+'.json | grep "result-dir/' + device_name + 'userdebug" | grep zip', shell=True, stdout=subprocess.PIPE).stdout.read()
# ----comment from ./bin/download-rom.sh 40 line ---BUILD=${line##*\/};BUILD=${BUILD%\"*}
sed_str = str('s/^.*\///g;s/\".*$//g')
build = subprocess.Popen(('{' + line + ' | sed ' + sed_str + '}'), shell=True, stdout=subprocess.PIPE).stdout.read()
print colored('Latest build is ' + build, 'red')

# If package not exist. Download it.
if os.path.exists(build):
    print "build file not exists, Download it."
    subprocess.call('wget --no-proxy --output-document=' + device + '.json http://android-ci-platform.marcus_chang.com/job/$artifact/lastSuccessfulBuild/api/json?pretty=true', shell=True)
path=str('result-dir_' + serialno);
if os.path.exists(path):
    shutil.rmtree(path)
# -------Not sure the unzip method is right,need debug.----------
# f = zipfile.ZipFile('filename.zip', 'w' ,zipfile.ZIP_DEFLATED)
# f.extractall([path[build]])
# f.close()
#----------------------------------------------------------------
subprocess.call('unzip ' + build +' -d' +path, shell=True)
print (device)
subprocess.call('popd > /dev/null', shell=True)

