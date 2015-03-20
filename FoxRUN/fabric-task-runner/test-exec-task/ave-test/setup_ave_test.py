__author__ = 'marcus chang (XP015317)'
__editor__ = 'tina2 zhao (XP015635)'

'''
Instead of the avetest/bin/setup-ave-test bash
This script is used for run the ave based mtbf, ui, endurance and performance test.
'''
import os
import time
import subprocess
from termcolor import colored
import sys
import util_ave
sys.path.append(util_ave.TESTTASKS_DIR)
import util_test

def start_ave_test(flash = 'false', precondition = 'false', gaiatest = 'true', test_type='ui', mtbf_time = '10h', iterations = '30', checkpoint = '10', app_name = 'all',b2gperf_test_type = 'startup'):
    '''
    #flash->boolean: false or true
    #precondition->boolean: false or true
    #gaiatest->boolean: false or true
    #test_type -> str like: [ui | mtbf | endurance | performance | b2gperf]
    #mtbf_time -> str like: '10h'
    #iterations -> int like: 30
    #checkpoint -> int like: 10
    #app_name -> str like: ['album.walkman.movies' for 3 apps | 'all' for all | 'ablum' for single app]
     '''

    # copy needed files
    if not os.path.exists(util_test.TESTSETAVE_UTILS_ROOT):
        subprocess.call('mkdir ' + util_test.TESTSETAVE_UTILS_ROOT, shell=True)

    if not os.path.exists(util_test.TESTSETAVE_UTILS_ROOT_BIN):
        subprocess.call('mkdir -p ' + util_test.TESTSETAVE_UTILS_ROOT_BIN, shell=True)

    if not os.path.exists(util_test.TESTSETAVE_UTILS_ROOT_PYTEST):
        subprocess.call('mkdir ' + util_test.TESTSETAVE_UTILS_ROOT_PYTEST, shell=True)

    #begin to copy all resources from avetest to the $HOME/.ave/webapptest
    copy_resources('fabric-task-runner', util_test.TESTSETAVE_UTILS_ROOT)
    copy_resources('Makefile', util_test.TESTSETAVE_UTILS_ROOT)
    copy_resources('test_media', util_test.TESTSETAVE_UTILS_ROOT)
    copy_resources('ApplicationList.ini', util_test.TESTSETAVE_UTILS_ROOT)
    copy_resources('pythontests/webapptest', util_test.TESTSETAVE_UTILS_ROOT_PYTEST)
    copy_resources('pythontests/requirements.txt', util_test.TESTSETAVE_UTILS_ROOT_PYTEST)
    copy_resources('pythontests/setup.py', util_test.TESTSETAVE_UTILS_ROOT_PYTEST)

    # Add command to workspace config: download-rom, precondition, run-ave-test
    handle_downloadrom_workspaceJSON = subprocess.Popen('grep "download-rom" ' + util_test.TESTSETAVE_WORKSPACE_ROOT + '/config/workspace.json', shell=True, stdout=subprocess.PIPE).stdout.read().strip('/n')
    handle_precondition_workspaceJSON = subprocess.Popen('grep "precondition" ' + util_test.TESTSETAVE_WORKSPACE_ROOT + '/config/workspace.json', shell=True, stdout=subprocess.PIPE).stdout.read().strip('/n')
    handle_runavetest_workspaceJSON = subprocess.Popen('grep "run-ave-test" ' + util_test.TESTSETAVE_WORKSPACE_ROOT + '/config/workspace.json', shell=True, stdout=subprocess.PIPE).stdout.read().strip('/n')
    if (handle_downloadrom_workspaceJSON == ''):
        subprocess.call('sed -i "s@\"tools\": {@\"tools\": {\n\t\"download-rom\":\"' + util_test.TESTSETAVE_UTILS_ROOT_BIN + '/download-rom\",@g" ' + util_test.TESTSETAVE_WORKSPACE_ROOT_CONFIG_JSON, shell=True)
    if (handle_precondition_workspaceJSON == ''):
        subprocess.call('sed -i "s@\"tools\": {@\"tools\": {\n\t\"precondition\":\"' + util_test.TESTSETAVE_UTILS_ROOT_BIN + '/precondition\",@g" ' + util_test.TESTSETAVE_WORKSPACE_ROOT_CONFIG_JSON, shell=True)
    if (handle_runavetest_workspaceJSON == ''):
        subprocess.call('sed -i "s@\"tools\": {@\"tools\": {\n\t\"run-ave-test\":\"' + util_test.TESTSETAVE_UTILS_ROOT_BIN + '/run-ave-test\",@g" ' + util_test.TESTSETAVE_WORKSPACE_ROOT_CONFIG_JSON, shell=True)

    # get phone count
    # subprocess.call('pushd ' + util_test.TESTSETAVE_UTILS_ROOT_BIN+' /ave-test' + ' > /dev/null', shell=True)
    # handle_ret = subprocess.Popen('vcsjob execute -j ./ -t get_workspace 2>&1', shell=True, stdout=subprocess.PIPE).stdout.read()
    # handle_num = subprocess.Popen('${' + handle_ret + '##*\ }', shell=True, stdout=subprocess.PIPE).stdout.read()
    # handle_len = subprocess.Popen('$((${#' + handle_num + '}-1))', shell=True, stdout=subprocess.PIPE).stdout.read()
    # handle_num_new = subprocess.Popen('${' + handle_num + ':0:' + handle_len + '}', shell=True, stdout=subprocess.PIPE).stdout.read()
    # print colored('phone count is ' + handle_num_new, 'red')
    subprocess.call('cd ' + util_test.TESTSETAVE_UTILS_ROOT_BIN+' /ave-test', shell=True)
    handle_rows = subprocess.Popen('adb devices|wc -l', shell=True, stdout=subprocess.PIPE).stdout.read()
    handle_num_new=int(handle_rows)-2
    print handle_num_new


    # parse arguments
    args_string_base = flash +','+ precondition+',' + gaiatest+','+ test_type +','+ app_name
    print colored('args_string_base---------------------->'+args_string_base,'red')
    envs_base = 'flash,precondition,gaiatest,test_type,app_name'
    args_string = ''
    envs = ''

    if(test_type == 'ui'):
        args_string = args_string_base
        envs = envs_base
    elif(test_type == 'endurance'):
        args_string = args_string_base + ','+ iterations + ',' + checkpoint
        envs = envs_base + ',iterations,checkpoint'
    elif(test_type == 'mtbf'):
        args_string = args_string_base + ',' + mtbf_time
        envs = envs_base+',mtbf_time'
    elif(test_type == 'b2gperf'):
        args_string = args_string_base +',' + iterations +','+ b2gperf_test_type
        envs = envs_base+',b2gperf_test_type'
    elif(test_type == 'performance'):
        args_string = args_string_base +','+ iterations
        envs = envs_base + ',iterations'
    else:
        print colored('options not supported, the @param test should be "ui, endurance, mtbf, b2gperf or performance"', 'red')

    print colored('args_string---------------------->'+args_string,'red')
    # envs = envs[:-1]
    cmdbody = "vcsjob execute -j ./ -t ave_test -e"
    cmd = args_string + ' ' + cmdbody + ' ' + envs
    print colored(cmd, 'red')

    # run test command
    print('handle_num_new-------------------->' + str(handle_num_new))
    if (handle_num_new==''):
        range_num=0
    else:
        range_num = handle_num_new
    print('range_num-------------------->' + str(range_num))
    for i in range(range_num):
        subprocess.call('gnome-terminal -x bash -c "' + cmd + ';read -p \'Press enter to exit\' -t 600" --tab --active', shell=True)
        print ('gnome cmd--->'+'gnome-terminal -x bash -c "' + cmd + ';read -p \'Press enter to exit\' -t 600" --tab --active')
        time.sleep(5)

    # subprocess.call('popd > /dev/null', shell=True)

def copy_resources(objfile, objlocation):
    print ('copy-------->''cp -rf ' + util_test.AVETEST_DIR + '/' + objfile + ' ' + objlocation)
    subprocess.call('cp -rf ' + util_test.AVETEST_DIR + '/' + objfile + ' ' + objlocation, shell=True)
