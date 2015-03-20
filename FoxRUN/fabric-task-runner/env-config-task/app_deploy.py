
'''
Instead of the avetest/bin/app-deploy bash
This script is used for webapps local deployment
'''

import os
import subprocess
import util_env
from termcolor import colored


def deploy_app():

    # to create base working directory
    if not os.path.exists(util_env.SETAPD_BASE_WORKING_DIRECTORY):
        print('to creat based working directory locally')
        subprocess.call('mkdir ' + util_env.SETAPD_BASE_WORKING_DIRECTORY, shell=True)
        subprocess.call('mkdir ' + util_env.SETAPD_BASE_WORKING_DIRECTORY_LOGS, shell=True)
        subprocess.call('mkdir ' + util_env.SETAPD_BASE_WORKING_DIRECTORY_PIDS, shell=True)
    else:
        print('working directory is already created locally')

    # to deploy webapps according to LOCAL_DEPLOYMENT_APP_NAME and DEPLOY_OPTIONS that we get from util_env.py
    # or to stop webapps according to LOCAL_DEPLOYMENT_APP_NAME and DEPLOY_OPTIONS that we get from util_env.py

    if (util_env.DEPLOY_OPTIONS == 'terminate'):
        print colored('we are going to stop webapps', 'red')
        if (util_env.LOCAL_DEPLOYMENT_APP_NAME == 'all'):
            index = 0
            for webapp_item in util_env.SETAPD_WEBAPPS_LIST:
                print colored('to stop ' + webapp_item, 'red')
                stop_app(webapp_item)
                index += 1
        else:
            index = 0
            for webapp_item in util_env.SETAPD_WEBAPPS_LIST:
                if (util_env.LOCAL_DEPLOYMENT_APP_NAME == webapp_item):
                    print colored('to stop ' + webapp_item, 'red')
                    stop_app(webapp_item)
                index += 1

    elif (util_env.DEPLOY_OPTIONS == 'default'):
        print colored('we are going to get and deploy webapps', 'green')
        if (util_env.LOCAL_DEPLOYMENT_APP_NAME == 'all'):
            subprocess.call('test -x ' + util_env.SETAPD_NODE + ' || exit 0', shell=True)
            index = 0
            for webapp_item in util_env.SETAPD_WEBAPPS_LIST:
                print colored('to get ' + webapp_item, 'green')
                get_app(webapp_item)
                print colored('to deploy ' + webapp_item, 'green')
                webapps_node_path = util_env.SETAPD_BASE_WORKING_DIRECTORY + webapp_item + '/dist/node_modules'
                if os.path.exists(webapps_node_path):
                    subprocess.call('pushd ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + webapp_item + '/dist/ > /dev/null', shell=True)
                    subprocess.call('npm install', shell=True)
                    subprocess.call('popd > /dev/null', shell=True)
                webapp_port = util_env.SETAPD_WEBAPPS_PORT[index]
                start_app(webapp_item, webapp_port)
                index += 1
        else:
            subprocess.call('test -x ' + util_env.SETAPD_NODE + ' || exit 0', shell=True)
            index = 0
            for webapp_item in util_env.SETAPD_WEBAPPS_LIST:
                if (util_env.LOCAL_DEPLOYMENT_APP_NAME == webapp_item):
                    print colored('to get ' + webapp_item, 'green')
                    get_app(webapp_item)
                    print colored('to deploy ' + webapp_item, 'green')
                    webapps_node_path = util_env.SETAPD_BASE_WORKING_DIRECTORY + webapp_item + '/dist/node_modules'
                    if os.path.exists(webapps_node_path):
                        subprocess.call('pushd ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + webapp_item + '/dist/ > /dev/null', shell=True)
                        subprocess.call('npm install', shell=True)
                        subprocess.call('popd > /dev/null', shell=True)
                    webapp_port = util_env.SETAPD_WEBAPPS_PORT[index]
                    start_app(webapp_item, webapp_port)
                index += 1

    elif (util_env.DEPLOY_OPTIONS == 'complete'):
        print colored('we are going to clone, build and deploy webapps', 'green')
        if (util_env.LOCAL_DEPLOYMENT_APP_NAME == 'all'):
            subprocess.call('test -x ' + util_env.SETAPD_NODE + ' || exit 0', shell=True)
            index = 0
            for webapp_item in util_env.SETAPD_WEBAPPS_LIST:
                print colored('to clone ' + webapp_item, 'green')
                clone_app(webapp_item)
                print colored('to build ' + webapp_item, 'green')
                build_app(webapp_item)
                print colored('to deploy ' + webapp_item, 'green')
                webapps_node_path = util_env.SETAPD_BASE_WORKING_DIRECTORY + webapp_item + '/dist/node_modules'
                if os.path.exists(webapps_node_path):
                    subprocess.call('pushd ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + webapp_item + '/dist/ > /dev/null', shell=True)
                    subprocess.call('npm install', shell=True)
                    subprocess.call('popd > /dev/null', shell=True)
                webapp_port = util_env.SETAPD_WEBAPPS_PORT[index]
                start_app(webapp_item, webapp_port)
                index += 1
        else:
            subprocess.call('test -x ' + util_env.SETAPD_NODE + ' || exit 0', shell=True)
            index = 0
            for webapp_item in util_env.SETAPD_WEBAPPS_LIST:
                if (util_env.LOCAL_DEPLOYMENT_APP_NAME == webapp_item):
                    print colored('to clone ' + webapp_item, 'green')
                    clone_app(webapp_item)
                    print colored('to build ' + webapp_item, 'green')
                    build_app(webapp_item)
                    print colored('to deploy ' + webapp_item, 'green')
                    webapps_node_path = util_env.SETAPD_BASE_WORKING_DIRECTORY + webapp_item + '/dist/node_modules'
                    if os.path.exists(webapps_node_path):
                        subprocess.call('pushd ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + webapp_item + '/dist/ > /dev/null', shell=True)
                        subprocess.call('npm install', shell=True)
                        subprocess.call('popd > /dev/null', shell=True)
                    webapp_port = util_env.SETAPD_WEBAPPS_PORT[index]
                    start_app(webapp_item, webapp_port)
                index += 1

    else:
        print('deployment options not support, it should be either default or complete')


############################################
# function to clone webapps projects by name
def clone_app(webapp):
############################################

#get app name
    appname = webapp
    appname_path = util_env.SETAPD_BASE_WORKING_DIRECTORY + appname
    if not os.path.exists(appname_path):
        subprocess.call('pushd ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + ' > /dev/null', shell=True)
        print colored('we are going to clone ' + appname, 'green')
        handleGitCloneWebApp = subprocess.Popen('git clone git@code.marcus_chang.com:webapps/' + appname + '.git', shell=True, stdout=subprocess.PIPE).stdout.read()
        if handleGitCloneWebApp == False:
            print colored('FATAL error: clone ' + appname + ' get failed', 'red')
        subprocess.call('popd > /dev/null', shell=True)
    else:
        print(appname + ' working directory does already exist')


############################################
# function to build webapps projects by name
def build_app(webapp):
############################################

#get app name
    appname = webapp
    appname_makefile_path = util_env.SETAPD_BASE_WORKING_DIRECTORY + appname + '/Makefile'
    if not os.path.exists(appname_makefile_path):
        print colored('FATAL error: can NOT make apps due to lack of Makefile', 'red')
    else:
        subprocess.call('pushd ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + appname + ' > /dev/null', shell=True)
        print('pull latest codes from remote repository')
        subprocess.call('git pull', shell=True)
        handleGitStatus = subprocess.Popen('git status | grep nothing', shell=True, stdout=subprocess.PIPE).stdout.read()
        if (handleGitStatus != '$NOTHING_TO_COMMIT'):
            print('clean ignored and non-igonored files so as to rebuild everything from scratch')
            subprocess.call('git clean -f -x', shell=True)
        else:
            print('working directory clean')
        print('we are going to make $appname in release mode')
        handleMakeRelease = subprocess.Popen('make release', shell=True, stdout=subprocess.PIPE).stdout.read()
        if handleMakeRelease == False:
            print colored('FATAL error: build $appname get failed', 'red')
        subprocess.call('popd > /dev/null', shell=True)


############################################
# function to get webapps projects by name
def get_app(webapp):
############################################

#get app name
    appname = webapp
    appname_path = util_env.SETAPD_BASE_WORKING_DIRECTORY + appname
    if not os.path.exists(appname_path):
        subprocess.call('pushd ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + ' > /dev/null', shell=True)
        subprocess.call('mkdir ' + appname, shell=True)
        subprocess.call('mkdir ' + appname + '/dist', shell=True)
        subprocess.call('popd > /dev/null', shell=True)
        subprocess.call('pushd ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + appname + '/dist' + ' > /dev/null', shell=True)
        webapp_build_download_url = 'http://android-ci.marcus_chang.com/job/webapps-' + appname + '/lastSuccessfulBuild/artifact/package.tgz'
        subprocess.call('wget -c ' + webapp_build_download_url, shell=True)
        subprocess.call('tar xf package.tgz', shell=True)
        subprocess.call('rm package.tgz', shell=True)
        subprocess.call('popd > /dev/null', shell=True)


############################################
# function to start webapps projects by name
def start_app(webapp, port):
############################################

#get app name and port
    appname = webapp
    appport = port
    PORT = appport + 'NODE_ENV=production "' + util_env.SETAPD_NODE + ' ' + util_env.SETAPD_BASE_WORKING_DIRECTORY + appname + '/dist/server.js" 1>>"' + util_env.SETAPD_BASE_WORKING_DIRECTORY_LOGS + appname + '.log" 2>&1 &'
    subprocess.call('echo $! > "' + util_env.SETAPD_BASE_WORKING_DIRECTORY_PIDS + appname + '.pid"', shell=True)


############################################
# function to stop webapps projects by name
def stop_app(webapp):
############################################

#get app name
    appname = webapp
    subprocess.call("kill 'cat " + util_env.SETAPD_BASE_WORKING_DIRECTORY_PIDS + appname + ".pid'", shell=True)










