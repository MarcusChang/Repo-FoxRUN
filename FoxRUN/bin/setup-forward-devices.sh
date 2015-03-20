#!/bin/bash

path=$1"/pythontests/pythonenv"
filename="marionette.py"
strsession="start_session(self, desired_capabilities=None):"
strsys="os.system"
condtion="        if (self.device_serial != None):\n"
forward="             os.system(\"adb -s \"+self.device_serial+\" forward tcp:2828 tcp:2828\")\n"


find $path -name $filename | while read line;
do
    grep -q $strsys $line ||
    {
        sed -i "s/$strsession/& \n$condtion$forward/" $line
    }
done