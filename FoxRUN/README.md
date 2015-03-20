# webapp test
#please note that "setup-forward-devices.sh" at "bin" folder is temporary workaround that modfiy marionette.py for gaiatest support multiple device test on one PC
#please note that "remove_gaiacode.sh" at "bin" folder is temporary workaround that modfiy taia_test.py for remove block code from gaiatest

## Set up environment for Firefox Marionette JS

    make install-xulrunner-sdk

## Set up environment for AVE Marionette Python

    make install-ave

## Set up environment for Webdriver Chrome Java

    make install-chromedriver

## Set up environment for Firefox addons

    make install-firefox-addons

## Run test based on Firefox Marionette JS

    make test-acceptance [APP= album | entrance | movies| walkman]

## Run test based on AVE Marionette Python

    make ave-marionette-test

## Run test based on Webdriver Chrome Java

    make webdriver-test

## To deploy all app locally
    
    make deploy-localapp [APP= album | entrance | movies| walkman] [OPTIONS=complete | terminate]
	
## Run performance test based on Firefox Marionette JS

    make test-perf [APP= album | entrance | movies| walkman] RUNS=run times(default is 5)

Just only for app memory and response time

## Run platform performance test based on Firefox Marionette JS

    make test-platform [APP= flipping_tiles | infinite_scroll | transitions_performance]

For app memory, cpu and frame rate

* **For phone:** script will install/replace isolate apps first.
* **For browser:** need to run firefox --marionette to start browser with marionette support.

## Run smoke test based on Firefox gaia ui test

    make gaia-ui-test [app_name=str,default is "all", means test all app you input] [device=str  serial identifier of device to target]
## Run endurance test based on Firefox gaia endurance test

    make gaia-endurance-test [iterations=ITERATIONS] [checkpoint=CHECKPOINT] [app_name=str,default is "all", means test all app you input] [device=str  serial identifier of device to target]

ITERATIONS and CHECKPOINT should be integer

## Run mtbf test based on Firefox MTBF-Driver

    make gaia-mtbf-test [MTBF_TIME=time] [app_name=str,default is "all", means test all app you input] [device=str  serial identifier of device to target]

time should like 2d(ay), 2h(our) or 2m(inute)

* **`mtbf_config.json`:** config what result we need include memory, logcat and etc. But Currently memory info can not get even set property as true and hack mtbf.py.
* **`mtbf.list`:** list test files to be run
* **`testvars.json`:** Set device info. details see offical document.

## Run b2gperf test based on Firefox gaia; ONLY focuse on launch time
    make gaia-b2gperf-test [iterations=int,default is 30 ] [app_name=str, example app_name=album,must be input appname for test,default is "all"] [test-type=str, default and only is startup] [device=str  serial identifier of device to target]

## Run performance test based on Firefox gaia; Focuse on Memory, CPU, Test Case running Time
    make gaia-performance-test [iterations=int,default is 30 ] [app_name=str,default is "all", means test all app you input] [device=str  serial identifier of device to target]

## Run ave based gaia python tests
    make ave-gaia-test [flash=true|false] [precondition=true|false] [gaiatest=true|false] [test-type=ui(default) | endurance | mtbf | b2gperf | performance] [app_name=str,default is "all", means test all app you input] [iterations=ITERATIONS] [checkpoint=CHECKPOINT] [MTBF_TIME=time]

flash: flash phone or not. default is false.
precondition: clear ftu; setup init settings; setup gaia test enviroment; push meida. default is false.
gaiatest: run test or not. defualt is true.
"test-type" and other parameters are used if "gaiatest" is "true". othewise is not necessary.

## Run gaia test under ave enviroment. It can run in different computer simultaneously. Before run test, you need to patch ave according to "update AVE" paragraph on https://wiki.marcus_chang.com/androiki/B2G/Testing/AVE-DUST/AST. then edit broker.json to add computeres to test network.

## Make precondiction before run test case
    make precondiction [device=str  serial identifier of device to target,for example:device=BL4610D16226]

## Flash device
    make flash [device=str  serial identifier of device to target,for example:device=BL4610D16226] [mgdir=str software path you want to flash,for example, imgdir=HELENIUM-2.0-140922-1618]

