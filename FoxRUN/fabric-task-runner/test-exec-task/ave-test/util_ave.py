#This module includes directory variables & const definition for pkg : ave-test
from fabric.api import *
import subprocess

HOME_DIR = subprocess.Popen('(cd ;pwd) | tr -d ["\n"]', shell=True, stdout=subprocess.PIPE).stdout.read()
AVETEST_DIR = subprocess.Popen('(cd ' + HOME_DIR + '/avetest;pwd) | tr -d ["\n"]', shell=True, stdout=subprocess.PIPE).stdout.read()
TESTTASKS_DIR = AVETEST_DIR + '/fabric-task-runner/test-exec-task/'

