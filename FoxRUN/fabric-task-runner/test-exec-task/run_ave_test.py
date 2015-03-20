
'''
Instead of the avetest/bin/run-ave-env bash
This script is used for run ave test
'''

import util_test
import subprocess
import sys
sys.path.append(util_test.ENVCFG_PATH)

def run_ave_test(test_type='ui', app_name='all', device='', iterations='30', checkpoint='10', mtbf_time='10h'):
    make_goal = 'gaia-' + test_type + '-test'
    make_params = 'app_name='+app_name+' device='+device
    if (test_type == 'endurance'):
        make_params = make_params + ' iterations='+iterations + ' checkpoint=' + checkpoint
    elif (test_type == 'mtbf'):
        make_params = make_params + ' MTBF_TIME=' + mtbf_time
    elif (test_type == 'b2gperf'):
        make_params = make_params + ' iterations=' + iterations
    elif (test_type == 'performance'):
        make_params = make_params + ' iterations=' + iterations

    subprocess.call('pushd '+util_test.TESTRUNAVE_UTILS_ROOT+' > /dev/null;'\
                    'make ' + make_goal+' ' + make_params+' #&> '+util_test.TESTRUNAVE_UTILS_ROOT + '/aaaaa.txt;'\
                    'popd > /dev/null', shell=True)