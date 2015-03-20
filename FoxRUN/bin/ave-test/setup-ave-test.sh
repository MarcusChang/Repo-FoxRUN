#!/bin/bash

WORKSPACE_ROOT=$HOME/.ave
UTILS_ROOT=$WORKSPACE_ROOT/webapptest
CURRENT_PATH=$(pwd)/`dirname $0`
BIN_PATH=$CURRENT_PATH/..
ROOT_PATH=$CURRENT_PATH/../..

# copy needed files
if [ ! -d $UTILS_ROOT ] ; then
    mkdir $UTILS_ROOT
fi
if [ ! -d $UTILS_ROOT/bin ] ; then
    mkdir -p $UTILS_ROOT/bin
fi
if [ ! -d $UTILS_ROOT/pythontests ] ; then
    mkdir $UTILS_ROOT/pythontests
fi

cp -rf $CURRENT_PATH $UTILS_ROOT/bin
cp -rf $BIN_PATH/precondition $UTILS_ROOT/bin
cp -rf $BIN_PATH/setup-gaiatest-env $UTILS_ROOT/bin
cp -rf $ROOT_PATH/Makefile $UTILS_ROOT
cp -rf $ROOT_PATH/test_media $UTILS_ROOT
cp -rf $ROOT_PATH/ApplicationList.ini $UTILS_ROOT
cp -rf $ROOT_PATH/pythontests/webapptest $UTILS_ROOT/pythontests
cp -rf $ROOT_PATH/pythontests/requirements.txt $UTILS_ROOT/pythontests
cp -rf $ROOT_PATH/pythontests/setup.py $UTILS_ROOT/pythontests
cp -rf $BIN_PATH/push-media $UTILS_ROOT/bin
cp -rf $BIN_PATH/setup-gaiatest-env $UTILS_ROOT/bin
cp -rf $BIN_PATH/setup-python-test $UTILS_ROOT/bin
cp -rf $BIN_PATH/run-ave-test $UTILS_ROOT/bin
cp -rf $BIN_PATH/config-init.sh $UTILS_ROOT/bin
cp -rf $BIN_PATH/remove_gaiacode.sh $UTILS_ROOT/bin
cp -rf $BIN_PATH/setup-forward-devices.sh $UTILS_ROOT/bin

# Add command to workspace config: download-rom, precondition, run-ave-test
if [ -z `grep "download-rom" $WORKSPACE_ROOT/config/workspace.json` ]; then
    sed -i "s@\"tools\": {@\"tools\": {\n\t\"download-rom\":\"$UTILS_ROOT/bin/ave-test/download-rom\",@g" $WORKSPACE_ROOT/config/workspace.json
fi
if [ -z `grep "precondition" $WORKSPACE_ROOT/config/workspace.json` ]; then
    sed -i "s@\"tools\": {@\"tools\": {\n\t\"precondition\":\"$UTILS_ROOT/bin/ave-test/precondition\",@g" $WORKSPACE_ROOT/config/workspace.json
fi
if [ -z `grep "run-ave-test" $WORKSPACE_ROOT/config/workspace.json` ]; then
    sed -i "s@\"tools\": {@\"tools\": {\n\t\"run-ave-test\":\"$UTILS_ROOT/bin/run-ave-test\",@g" $WORKSPACE_ROOT/config/workspace.json
fi

# get phone count
pushd $UTILS_ROOT/bin/ave-test > /dev/null
ret=`vcsjob execute -j ./ -t get_workspace 2>&1`
num=${ret##*\ }
len=$((${#num}-1))
num=${num:0:len}
echo "phone count is $num"

# parse arguments
declare -a ARGS=(flash precondition gaiatest test_type app_name iterations checkpoint MTBF_TIME)
args=$@
envs=""
while [ ! -z $1 ]; do
    arg=${1##*=}
    for ARG in "${ARGS[@]}"; do
        case $1 in
            $ARG=*)
                envs=$envs$ARG,; break;;
        esac
    done
    shift
done
envs=${envs%,*}
cmdbody="vcsjob execute -j ./ -t ave_test -e"
cmd="$args $cmdbody $envs"
echo $cmd

# run test command
for((i=0;i<$num;i++))
do
    gnome-terminal -x bash -c "$cmd;read -p 'Press enter to exit' -t 600" --tab --active
    sleep 5
done

popd > /dev/null

