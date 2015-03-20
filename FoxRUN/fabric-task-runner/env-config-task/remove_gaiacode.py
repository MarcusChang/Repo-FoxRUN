#!/usr/bin/python
__author__ = 'Jay (XP016283)'

'''
Instead of the avetest/bin/remove_giacode.sh
This script is used for .
'''

import os
import util_env
import subprocess
from termcolor import colored
import sys



def remove_gaiacode(path1 = util_env.AVETEST_DIR):
    filename='gaia_test.py'
    remove_contacts='            self.data_layer.remove_all_contacts()'
    remove_contacts_hash='            #self.data_layer.remove_all_contacts()'
    path= path1+'/pythontests/pythonenv'

    print ('find cmd:-------->''find ' + path +' -name ' + filename + '')
    file=subprocess.Popen('find ' + path +' -name ' + filename + '', shell=True, stdout=subprocess.PIPE).stdout.read()
    print(file)
    file_list=file.strip('\n')
    file_list_1=file_list.split('\n')

    print(file_list_1)

    for i in file_list_1:
        subprocess.call('sed -i "/^' + remove_contacts +'/ c\\'+remove_contacts_hash+'" ' + i, shell=True)
        print ('sed cmd:----->' 'sed -i "/^' + remove_contacts +'/ c\\'+remove_contacts_hash+'" ' + i)

# def main():
#     remove_gaiacode()
#
# main()