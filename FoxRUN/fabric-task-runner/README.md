# webapp test : fabric_task_runner - Tutorial

## To Setup the Fabric environment you need to do below things:
    --> For fabric environment setup, please go to the "/home/CORPUSERS/XXX/avetest/fabric-task-runner/Fabric-Env".
       *The "XXX" is your linux login user name*
    1. Copy the ez_setuptools folder from Fabric-Env to the /home/CORPUSERS/XXX and move into it then input the cmd : "sudo python ./ez_setuptools/ez_setup.py" to install the python setuptools.
    2. Uncompress the "paramiko-1.14.0.tar.gz" in the "Fabric-Env.rar" to /home/CORPUSERS/XXX, then run the cmd : "sudo easy_install /home/CORPUSERS/XXX/paramiko-1.14.0"
    3. Uncompress the "termcolor-1.1.0.tar.gz" in the attachment to /home/CORPUSERS/XXX, then run the cmd : "sudo easy_install /home/CORPUSERS/XXX/termcolor-1.1.0"
    4. Uncompress the "Fabric-1.9.1.tar.gz" in the "Fabric-Env.rar" to /home/CORPUSERS/XXX, then run the cmd : "sudo easy_install /home/CORPUSERS/XXX/Fabric-1.9.1"

    To test whether you have installed the Fabric-1.9.1, you can run below cmds :

    XXX@cnbjlx *:~$ which fab
    /user/local/bin/fab

    Then you can create a simple test script like : test.py includes below content: def test():
    print("the fab has installed!")

    Then run the cmd : fab -f test.py test


## Set up environment for Firefox Marionette JS

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/env-config-task
    fab -f setup_xulrunner.py xulrunner_setup
    *The "XXX" is your linux login user name*

## Set up environment for AVE Marionette Python

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/env-config-task
    fab -f setup_ave.py ave_setup

## Set up environment for Webdriver Chrome Java

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/env-config-task
    fab -f setup_chromedriver.py chromedriver_setup

## Set up environment for Firefox addons

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/env-config-task
    fab -f setup_firefox_addons.py firefox_addons_setup

## Run test based on Firefox Marionette JS

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/test-exec-task
    fab -f gaia_marionette.py marionette_gaia:[album | walkman | movies],test-acceptance,[device | firefox]

## Run test based on AVE Marionette Python

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/test-exec-task
    fab -f ave_marionette.py ave_marionette_test

## Run test based on Webdriver Chrome Java

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/test-exec-task
    fab -f webdriver_chrome.py webdriver_chrome_test

## To deploy all app locally

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/env-config-task
    fab -f app_deploy.py deploy_app
    *To choose which app to be deployed and the deploy options: modify the value of "util_env.LOCAL_DEPLOYMENT_APP_NAME" and "util_env.DEPLOY_OPTIONS"*

## Run performance test based on Firefox Marionette JS (Just only for app memory and response time)

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/test-exec-task
    fab -f gaia_perf_marionette.py test_perf:[album | walkman | movies],10
    *The second parameter '10' means 10 sec*

## Run platform performance test based on Firefox Marionette JS

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/test-exec-task
    fab -f gaia_marionette.py marionette_gaia:[flipping_tiles | infinite_scroll | transitions_performance],test-platform,[device | firefox]

    For app memory, cpu and frame rate

    *For phone:** script will install/replace isolate apps first.*
    *For browser:** need to run firefox --marionette to start browser with marionette support.*

## Run smoke test based on Firefox gaia ui | endurance | mtbf | performance test

    cd /home/CORPUSERS/XXX/avetest/fabric-task-runner/test-exec-task
    fab -f setup_python_test.py start_python_test:[ui | mtbf | endurance | performance],10h,30,10,[album | walkman | movies]

    test -> str like: [ui | mtbf | endurance | performance]
    mtbf_time -> str like: '10h' , time should like 2d(ay), 2h(our) or 2m(inute)
    iterations -> int like: 30
    checkpoint -> int like: 10
    app_name -> str like: 'album', 'walkman', 'movies'

    *`mtbf_config.json`:** config what result we need include memory, logcat and etc. But Currently memory info can not get even set property as true and hack mtbf.py*
    *`mtbf.list`:** list test files to be run*
    *`testvars.json`:** Set device info. details see offical document.*
    *`AtcMtbfTestCase.py`:** Inherit from MtbfTestCase of MTBF-Driver. Overide cleanup_gaia method to avoid close wifi*
