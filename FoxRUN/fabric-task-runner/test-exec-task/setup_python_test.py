
'''
Instead of the avetest/bin/setup-python-test bash
This script is used for run the mtbf, ui, endurance and performance test.
'''

import os
import util_test
import subprocess
from termcolor import colored
import sys
import time
sys.path.append(util_test.ENVCFG_PATH)
import push_media

def start_python_test(test_type='ui', mtbf_time = '10h', iterations = '2', checkpoint = '2', app_name = 'all', device = None):

    '''
    #test -> str like: [ui | mtbf | endurance | performance | b2gperf]
    #mtbf_time -> str like: '10h'
    #iterations -> int like: 30
    #checkpoint -> int like: 10
    #app_name -> str like: 'album','album.walkman.movies' or 'all'
    #device -> device-serial str like:
    '''

    # subprocess.call('source ' + util_test.TESTSETPY_TEST_PATH + '/pythonenv/bin/activate', shell=True)
    if app_name == 'all':
        handle_application_ini_path = subprocess.Popen('grep -c . ' + util_test.AVETEST_DIR + '/ApplicationList.ini', shell=True, stdout=subprocess.PIPE).stdout.read()
        if int(handle_application_ini_path) <= 1:
            print colored('Please firstly add test target application name at ' + util_test.AVETEST_DIR + '/ApplicationList.ini, or input application name at terminal', 'red')
    elif app_name == '':
        print colored('Please input right paramter terminal after call command , for example "fab -f setup_python_test.py start_python_test:ui,walkman.album,null"')

    #the device serial is mandatory on Jenkins, otherwise is optional
    if device == None:
        device_param = ''
        adb_device = ''
    else:
        if test_type == 'b2gperf':
            device_param = '--device-serial=' + device
        else:
            device_param = '--device=' + device
        adb_device = '-s ' + device

    # subprocess.call('source ' + util_test.TESTSETPY_TEST_PATH + '/pythonenv/bin/activate;'+'adb ' + adb_device + ' root', shell=True)
    # time.sleep(1)
    # subprocess.call('source ' + util_test.TESTSETPY_TEST_PATH + '/pythonenv/bin/activate;'+'adb ' + adb_device + ' forward tcp:2828 tcp:2828', shell=True)
    source_adb_cmd='source ' + util_test.TESTSETPY_TEST_PATH + '/pythonenv/bin/activate;' + 'adb ' + adb_device + ' root;'+'sleep 1;'+'adb ' + adb_device + ' forward tcp:2828 tcp:2828;'

    #add target application into ".ini" file
    config_init_path = util_test.AVETEST_DIR + '/fabric-task-runner/env-config-task/config_init.py'
    subprocess.call(source_adb_cmd + 'python ' + config_init_path + ' ' + app_name + ' ' + util_test.AVETEST_DIR, shell=True)

    #install test target app according to app install list file "ApplicationList.ini"
    #subprocess.call('source ' + util_test.TESTSETPY_TEST_PATH + '/pythonenv/bin/activate;''python ' + util_test.TESTSETPY_WEBAPP_TEST + 'mixins/install.py --filename=' + util_test.AVETEST_DIR + '/ApplicationList.ini' + ' --testvars=' + util_test.TESTSETPY_WEBAPP_TEST + '/testvars.json', shell=True)
    # print ('install.py------------->'+'python ' + util_test.TESTSETPY_WEBAPP_TEST + 'mixins/install.py --filename=' + util_test.AVETEST_DIR + '/ApplicationList.ini' + ' --testvars=' + util_test.TESTSETPY_WEBAPP_TEST + 'testvars.json')

    #modfiy marionette.py so that it can support multiple devices test on one PC
    setup_forword_devices_path = util_test.AVETEST_DIR + '/fabric-task-runner/env-config-task/setup_forward_devices.py'
    subprocess.call(source_adb_cmd + 'python ' + setup_forword_devices_path + ' ' + util_test.AVETEST_DIR, shell=True)

    remove_gaiacode_path = util_test.AVETEST_DIR + '/fabric-task-runner/env-config-task/remove_gaiacode.py'
    subprocess.call(source_adb_cmd + 'python ' + remove_gaiacode_path + ' ' + util_test.AVETEST_DIR, shell=True)

    gen_param = '--address=localhost:2828  ' + device_param +' --testvars=' + util_test.TESTSETPY_WEBAPP_TEST + 'testvars.json --timeout=60000 --html-output=result-`date +%y%m%d%H%M%S`.html'

    if test_type == 'ui':
        print colored('ui test begin!', 'red')
        push_media.media_push(device)
        print ('pushd ui-------'+'pushd ' + util_test.TESTSETPY_WEBAPP_TEST + 'ui > /dev/null')
        print ('gaiatest --type=b2g ' + gen_param + ' manifest.ini')
        subprocess.call(source_adb_cmd + 'pushd ' + util_test.TESTSETPY_WEBAPP_TEST + 'ui > /dev/null;''gaiatest --type=b2g ' + gen_param + ' manifest.ini;''popd > /dev/null', shell=True)
        # subprocess.call('gaiatest --type=b2g ' + gen_param + ' manifest.ini', shell=True)
        # subprocess.call('popd > /dev/null', shell=True)

    elif test_type == 'endurance':
        print colored('endurance test begin!', 'red')
        push_media.media_push(device)
        subprocess.call(source_adb_cmd + 'pushd ' + util_test.TESTSETPY_WEBAPP_TEST + 'endurance > /dev/null;'+'gaiatest --type=b2g ' + gen_param + ' --iterations=' + iterations + ' --checkpoint=' + checkpoint + ' manifest.ini;'+'popd > /dev/null', shell=True)
        # subprocess.call('gaiatest --type=b2g ' + gen_param + ' --iterations=' + iterations + ' --checkpoint=' + checkpoint + ' manifest.ini', shell=True)
        # subprocess.call('popd > /dev/null', shell=True)

    elif test_type == 'mtbf':
        print colored('mtbf test begin!', 'red')
        push_media.media_push(device)
        subprocess.call(source_adb_cmd + 'pushd ' + util_test.TESTSETPY_WEBAPP_TEST + 'mtbf > /dev/null;''MTBF_TIME=' + mtbf_time + ' MTBF_CONF=mtbf_config.json mtbf ' + gen_param + ' ./;'+'popd > /dev/null', shell=True)
        # subprocess.call('MTBF_TIME=' + mtbf_time + ' MTBF_CONF=mtbf_config.json mtbf ' + gen_param + ' ./', shell=True)
        # subprocess.call('popd > /dev/null', shell=True)

    elif test_type == 'performance':
        print colored('performance test begin!', 'red')
        push_media.media_push(device)
        subprocess.call(source_adb_cmd + 'pushd ' + util_test.TESTSETPY_WEBAPP_TEST + 'performance > /dev/null;''gaiatest --type=b2g ' + gen_param + ' --iterations=' + iterations + ' manifest.ini;'+'popd > /dev/null', shell=True)
        # subprocess.call('gaiatest --type=b2g ' + gen_param + ' --iterations=' + iterations + ' manifest.ini', shell=True)
        # subprocess.call('popd > /dev/null', shell=True)

    elif test_type == 'b2gperf':
        print colored('b2gperf test begin!', 'red')
        push_media.media_push(device)
        application_list_ini_path = util_test.AVETEST_DIR + '/ApplicationList.ini'
        open_applist_ini = open(application_list_ini_path, 'r')
        for line in open_applist_ini.readlines():
            if line != None or line != '':
                subprocess.call('b2gperf ' + line + ' ' + device_param + ' --testvars=' + util_test.TESTSETPY_WEBAPP_TEST + '/testvars.json --iterations=' + iterations + ' --no-restart', shell=True)

    else:
        print colored('options not support', 'red')





