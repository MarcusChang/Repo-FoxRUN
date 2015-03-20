#!/usr/bin/python

import os
import sys
import time
import re
import multiprocessing as mp
import shutil
import stat
import traceback
import urllib
import subprocess
import time
import commands
import urllib
import zipfile

import vcsjob
import ave.label
import ave.c2d
from ave.broker import Broker
from ave.broker.exceptions import Busy
from ave.workspace import Workspace
from ave.exceptions import Timeout, Terminated

def push_setflag(handset, workspace):
    # figure out if we need to download and push setflag to the handset. it
    # is harmless to execute setflag without options but raises an exception
    # if the executable is not available on the handset.
    try:
        handset.shell('setflag')
        push_setflag = False
    except Exception, e:
        if str(e).startswith('no such executable'):
            push_setflag = True
        else:
            raise e
    if push_setflag:
        # Any setflag package will work. Because there is no setflag package
        # related to inofficial branches, the latest label from the official
        # jb-mr2-yukon branch is used for retrieving setflag.
        setflag_label   = get_latest_label('kk-yukon')
        setflag_package = 'mw-setflag-proto_t-eng-release'
        path = workspace.download_c2d_regexp(setflag_package,
            label=setflag_label, timeout=30)
        # unpack the binary and push it to the handset. unfortunately we need
        # some intimate knowledge about where the binary is found inside the
        # package, but this determined entirely by the build system and would
        # normally never change, so it should be ok:
        path = workspace.unpack_c2d(path)
        path = os.path.join(path,'imgdata','system','bin','setflag')
        try:
            handset.root()
            handset.remount()
            handset.push(path, '/system/bin/setflag')
        except Exception, e:
            print('FAIL %s: could not push setflag: %s' % e)
            return False
    return True

# Will try to get the latest official label, on failure it will try to get the
# latest unofficial label.
def get_latest_label(branch, model=None):
    try:
        label = ave.label.get_latest(branch)
    except Exception, e:
        if 'Failed to get latest software label' in str(e):
            cmd = 'repository listlabels -b %s -prod %s | tail -1'\
                % (branch.lower(), model)
            label = subprocess.check_output(cmd, shell=True)
            label = label.rstrip()
        else:
            raise e
    return label

def download_zip(workspace, build):
    image_dir = workspace.download_jenkins(
                 job_id = 'daily_build_ffos',
                 build_id = 'lastSuccessfulBuild',
                 timeout = 300,
                 artifacts = ['result-dir/%s' %build],
                 base = 'http://android-ci-platform.marcus_chang.com')
    image_dir = os.path.join(workspace.get_path(), image_dir)
    return image_dir

def save_handset_serial():
    temp_workspace = Workspace()
    serial = handset.get_profile()['serial']
    serial_file_path = os.path.join(temp_workspace.root, 'serial.txt')
    file = open(serial_file_path, 'w')
    file.write("%s\n" % serial)
    file.close()
    print('Handset serial %s has been saved in %s' % (serial, serial_file_path) )
    temp_workspace.delete()

# Flash device with the latest label
# fg3console has to be started before flashing is possible, run:
# fg3console -dm &
def flash_device(workspace, handset, image_dir):
    if not push_setflag(handset, workspace):
        return False
    model = handset.get_profile()['pretty']
    log = handset.flash_directory(image_dir, False)
    sys.stdout.write(log)
    sys.stdout.flush()
    while True:
        try:
            log = handset.get_flash_log(2)
            sys.stdout.write(log)
            sys.stdout.flush()
            if 'Error:' in log:
                print('FAIL %s: Error detected: %s' % e)
                return False
        except Timeout:
            continue
        except Terminated:
            break
        except Exception, e:
            print('FAIL %s: could not flash image: %s' % e)
            traceback.print_exc()
            return False
    try:
        handset.wait_power_state('boot_completed', timeout=200)
    except Exception, e:
        print('FAIL: waiting for reboot to finish failed: %s' % e)
        return False
    return True

url_base = "http://android-ci-platform.marcus_chang.com/job/"
api_suffix = "/lastSuccessfulBuild/api/python"
file_suffix = "/lastSuccessfulBuild/artifact/result-dir/"
url_branch = {
    "proto_f" : "daily_build_helenium",
    "proto_t" : "daily_build_ffos",
}

def get_build(handset):
    api = urllib.urlopen(url_base + url_branch[handset.profile["pretty"]] + api_suffix).read()
    build = ""
    ll = eval(api)["artifacts"]
    for element in ll:
        if (element["fileName"].find("userdebug") > 0 and element["fileName"].find(".zip") > 0):
            build = element["fileName"]
            break
    return build

def download_zip2(handset, build):
    #download file and unzip
    file11 = urllib.urlretrieve(url_base + url_branch[handset.profile["pretty"]] + file_suffix + build, handset.profile["pretty"] + ".zip")
    f = zipfile.ZipFile(build, "r")
    for file in f.namelist():
        f.extract(file, "temp1/")

def runtest(workspace, handset):
    test_type = os.getenv("test_type")
    app_name = os.getenv("app_name")
    device = handset.profile["serial"]
    iterations = os.getenv("iterations")
    checkpoint = os.getenv("checkpoint")
    MTBF_TIME = os.getenv("MTBF_TIME")

    cmds = {
        'ui': "run-ave-test %s %s %s" % (test_type, app_name, device),
        'endurance': "run-ave-test %s %s %s %s %s" % (test_type, app_name, device, iterations, checkpoint),
        'mtbf': "run-ave-test %s %s %s %s" % (test_type, app_name, device, MTBF_TIME),
        'performance': "run-ave-test %s %s %s %s" % (test_type, app_name, device, iterations),
        'b2gperf': "run-ave-test %s %s %s %s" % (test_type, app_name, device, iterations),
    }
    cmd = cmds[test_type]
    print cmd
    res = workspace.run(cmd)
    print res[1]

def test_process(workspace, handset):
    flash = os.getenv("flash")
    precondition = os.getenv("precondition")
    gaiatest = os.getenv("gaiatest")
    if flash == None:
        flash = "false"
    if precondition == None:
        precondition = "false"
    if gaiatest == None:
        gaiatest = "true"
    if flash == "true":
        # Run preconditon after flash
        precondition = "true"

    if flash == "true":
        path = os.path.realpath(os.path.dirname(__file__))
        image_dir = os.path.join(path, 'result-dir_' + handset.profile["serial"])
        # Download image. It should be handled by python. But currently workspace.download_jenkins
        # function does not work due to do not know how to config jenkins.json. So use a shell replace
        cmd = "download-rom " + handset.profile["serial"]
        res = workspace.run(cmd)
        print res[1]
        result = flash_device(workspace, handset, image_dir)
        time.sleep(30)
    if precondition == "true":
        cmd = "precondition " + handset.profile["serial"]
        res = workspace.run(cmd)
        print res[1]
        time.sleep(30)
    if gaiatest == "true":
        runtest(workspace, handset)

def main():
    prf = vcsjob.get_profiles()
    b = Broker()
    workspace, handset = b.get({'type':'workspace'}, {'type':'handset', 'platform':'firefox'})
    print "\nHost: %s" % handset.address[0]
    print "Device model: %s" % handset.profile["pretty"]
    print "Device serial: %s\n" % handset.profile["serial"]
    test_process(workspace, handset)

if __name__ == '__main__':
    main()

