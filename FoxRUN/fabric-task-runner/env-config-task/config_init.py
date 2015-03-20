__author__ = 'Jay (XP016283)'

'''
Instead of the avetest/bin/config-init.sh
This script is used for adding the parmater from user input into config file, "manifest.ini" and "mtbf.list","ApplicationList.ini"
'''
import sys
import subprocess
import util_env
import re

def config_init(app_name = 'all', path = util_env.AVETEST_DIR):
    print ('path-----'+path)
    webapp_path = path+'/pythontests/webapptest'
    suffix = '.py'
    prefix = 'test_'
    applist = []
    #   app_name = sys.argv[1]
    print ('appname-------->'+app_name)

    if (app_name == 'all'):
        all_apps = path+'/ApplicationList.ini'
        f = open(all_apps, 'r')
        for line in f.readlines()[1:]:
            if (line!='\n'):
                applist.append(line.strip('\n'))
            # applist = re.findall("^[A-Za-z]\n", line)
        f.close()
        print applist

    else:
        applist = app_name.split('.')
        print('applist---------------->'+ str(applist))
        # sed_str=str('/^[a-z]/d')
        # subprocess.call('sed -i' + sed_str +' '+ path +'/ApplicationList.ini', shell=True)
        #applist=${app_name//','/' '}


#modify "mtbf.list" in webapptest dir
    mlist=webapp_path+'/mtbf/mtbf.list'
    f=open(mlist,'w')
    mlist_a=['{ \"runlist\": [\n']
    f.writelines(mlist_a)
    f.close()

    for app in applist:
        f=open( mlist,'a')
        mlist_b=['\"'+prefix+app+suffix+'\",\n']
        f.writelines(mlist_b)
        f.close()
#delete the last 2 char - "," and "\n"
    f= open(mlist,'r').read()
    f_delete_last_char=f[:-2]
    f=open(mlist,'w')
    mlist_c=[f_delete_last_char+'\n'+']\n}\n']
    f.writelines(mlist_c)
    f.close()

#modify "manifest.ini" at "webapptest" dir
    manifest_inis=[webapp_path+'/endurance/manifest.ini', webapp_path + '/performance/manifest.ini', webapp_path + '/ui/manifest.ini']
    for manifest_ini in manifest_inis:
        f=open(manifest_ini,'w')
        de=['[DEFAULT]\n','b2g = true\n','carrier = false\n','# online = true\n','# lan = true\n','# online = false\n','# offline = false\n','wifi = true\n','smoketest = false\n']
        f.writelines(de)
        f.close()
        for app in applist:
            f=open(manifest_ini,'a')
            li='['+prefix+app+suffix+']\n'
            f.writelines(li)
            f.close()

#modify "ApplicationList.ini" at "avetest" dir
    Applist_inis=[path+'/ApplicationList.ini']
    for Applist_ini in Applist_inis:
        f=open(Applist_ini,'w')
        l=['#Applist\n']
        f.writelines(l)
        f.close()
        for app in applist:
            f=open(Applist_ini,'a')
            li=[app+'\n']
            f.writelines(li)
            f.close()


def main():
   config_init()


main()














