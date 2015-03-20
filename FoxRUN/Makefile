##################################################################################
# Global Variables:                                                              #
# TEST_MANIFEST: Backlist                                                        #
# REPORTER: Use 'spec' for marionette-mocha which wrapped mocha                  #
# MARIONETTE_RUNNER_HOST : The Marionnette runner host.                          #
#                          Current values can be 'marionette-b2gdesktop-host'    #
#                          , 'marionette-device-host' or marionette-firefox-host #
# DEPLOY_OPTION : 'complete' means clone + build + deploy app                    #
#                 'default' means deploy app                                     #
#                 'terminate' means stop app                                     #
##################################################################################
MARIONETTE_RUNNER_HOST?=marionette-device-host
TEST_MANIFEST?=./config/test-manifest.json
REPORTER?=spec
TEST_ACCEPTANCE_APP_NAME?=*
TEST_PERFORMANCE_APP_NAME?=$(shell find tests -type d -name 'performance' | sed -e 's|^tests/||' -e 's|/performance$$||' )
MOZPERFOUT?=perfreport
LOCAL_DEPLOYMENT_APP_NAME?=all
DEPLOY_OPTIONS?=default
APP_NEED_PUSH=all
ifneq ($(APP),)
	ifeq ($(MAKECMDGOALS), test-acceptance)
	TEST_ACCEPTANCE_APP_NAME=$(APP)
	APP_NEED_PUSH=$(APP)
	endif
	ifeq ($(MAKECMDGOALS), test-platform)
	TEST_ACCEPTANCE_APP_NAME=$(APP)
	endif
	ifeq ($(MAKECMDGOALS), test-perf)
	TEST_PERFORMANCE_APP_NAME=$(APP)
	endif
	ifeq ($(MAKECMDGOALS), deploy-localapp)
	LOCAL_DEPLOYMENT_APP_NAME=$(APP)
	endif
	ifeq ($(MAKECMDGOALS), install-platform-app)
	LOCAL_DEPLOYMENT_APP_NAME=$(APP)
	endif
endif

ifneq ($(OPTIONS),)
	ifeq ($(MAKECMDGOALS), deploy-localapp)
	DEPLOY_OPTIONS=$(OPTIONS)
	endif
endif

ifeq ($(MAKECMDGOALS), gaia-mtbf-test)
	ifeq ($(MTBF_TIME),)
	    MTBF_TIME=10h
	endif
endif

ifeq ($(MAKECMDGOALS), gaia-endurance-test)
	ifeq ($(checkpoint),)
	    checkpoint=5
	endif
endif

ifeq ($(MAKECMDGOALS), gaia-b2gperf-test)
	ifeq ($(b2gperf-test-type),)
	    b2gperf-test-type=startup
	endif
endif

ifeq ($(iterations),)
    iterations=30
endif

ifeq ($(app_name),)
    app_name=all
endif

ifeq ($(device),)
    device=none
endif

ifeq ($(MAKECMDGOALS), ave-gaia-test)

	ifeq ($(precondition),)
		precondition=false
	endif
	ifeq ($(gaiatest),)
		gaiatest=true
	endif
	ifeq ($(gaiatest), true)
	    ifeq ($(test_type),)
		    test_type=ui
	    endif
        ave_test_params_common=precondition=$(precondition) gaiatest=$(gaiatest) test_type=$(test_type) app_name=$(app_name)

	    ifeq ($(test_type), ui)
            ave_test_params=$(ave_test_params_common)
	    endif

	    ifeq ($(test_type), endurance)
		    ifeq ($(checkpoint),)
			    checkpoint=10
		    endif
		    ave_test_params=$(ave_test_params_common) iterations=$(iterations) checkpoint=$(checkpoint)
	    endif

	    ifeq ($(test_type), mtbf)
		    ifeq ($(MTBF_TIME),)
			    MTBF_TIME=10h
		    endif
		    ave_test_params=$(ave_test_params_common) MTBF_TIME=$(MTBF_TIME)
	    endif

	    ifeq ($(test_type), performance)
		    ave_test_params=$(ave_test_params_common) iterations=$(iterations)
	    endif

	    ifeq ($(test_type), b2gperf)
		    ifeq ($(b2gperf-test-type),)
			    b2gperf-test-type=startup
		    endif
		    ave_test_params=$(ave_test_params_common) iterations=$(iterations) b2gperf-test-type=$(b2gperf-test-type)
	    endif
	else
	    ave_test_params=precondition=$(precondition) gaiatest=$(gaiatest)
	endif
endif

###############################################################################
# Tests                                                                       #
###############################################################################
.PHONY: test-acceptance
# $(PROFILE_FOLDER) should be `profile-test` when we do `make test-acceptance`.
#test-acceptance: b2g $(PROFILE_FOLDER)
test-acceptance: install-xulrunner-sdk
	./bin/push-media $(APP_NEED_PUSH) $(MARIONETTE_RUNNER_HOST) $(device)
	./bin/gaia-marionette $(shell find . -path "*$(TEST_ACCEPTANCE_APP_NAME)/marionette/*_test.js") \
		--host $(MARIONETTE_RUNNER_HOST) \
		--manifest $(TEST_MANIFEST) \
		--reporter $(REPORTER)

.PHONY: test-platform
test-platform: install-xulrunner-sdk install-platform-app
	./bin/gaia-marionette $(shell find . -path "*$(TEST_ACCEPTANCE_APP_NAME)/platform/*_test.js") \
		--host $(MARIONETTE_RUNNER_HOST) \
		--manifest $(TEST_MANIFEST) \
		--reporter $(REPORTER)

.PHONY: gaia-mtbf-test
gaia-mtbf-test:
	./bin/setup-python-test mtbf $(app_name) $(device) $(MTBF_TIME)

.PHONY: gaia-ui-test
gaia-ui-test:
	./bin/setup-python-test ui $(app_name) $(device)

.PHONY: gaia-endurance-test
gaia-endurance-test:
	./bin/setup-python-test endurance $(app_name) $(device) $(iterations) $(checkpoint)

.PHONY: gaia-performance-test
gaia-performance-test:
	./bin/setup-python-test performance $(app_name) $(device) $(iterations)

.PHONY: gaia-b2gperf-test
gaia-b2gperf-test:
	./bin/setup-python-test b2gperf $(app_name) $(device) $(iterations) $(b2gperf-test-type)

.PHONY: ave-marionette-test
ave-marionette-test: install-ave
	./bin/ave-marionette

.PHONY: webdriver-chrome-test
webdriver-chrome-test: install-chromedriver
	./bin/webdriver-chrome

.PHONY: test-perf
test-perf:
	MOZPERFOUT="$(MOZPERFOUT)" APPS="$(TEST_PERFORMANCE_APP_NAME)" MARIONETTE_RUNNER_HOST=$(MARIONETTE_RUNNER_HOST) GAIA_DIR="`pwd`" ./bin/gaia-perf-marionette

PHONY: ave-gaia-test
ave-gaia-test:
	./bin/ave-test/setup-ave-test.sh $(ave_test_params)

.PHONY: setup-gaia-env
setup-gaia-env:
	./bin/setup-gaiatest-env

.PHONY: precondition
precondition: setup-gaia-env
	#make precondiction and skip firefox user tutorial
	./pythontests/pythonenv/bin/python ./bin/precondition/precondition.py --device-serial=$(device)

###############################################################################
# Utilities                                                                       #
###############################################################################
.PHONY: install-xulrunner-sdk
install-xulrunner-sdk:
	./bin/setup-xulrunner

.PHONY: install-ave
install-ave:
	./bin/setup-ave

.PHONY: install-platform-app
install-platform-app:
	./bin/setup-platform $(LOCAL_DEPLOYMENT_APP_NAME)

.PHONY: install-chromedriver
install-chromedriver:
	./bin/setup-chromedriver

.PHONY: install-firefox-addons
install-firefox-addons:
	./bin/setup-firefox-addons

.PHONY: deploy-localapp
deploy-localapp: install-firefox-addons
	./bin/app-deploy $(LOCAL_DEPLOYMENT_APP_NAME) $(DEPLOY_OPTIONS)
