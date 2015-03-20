#!/bin/bash

path=$1"/pythontests/pythonenv"

filename="gaia_test.py"

remove_contacts="            self.data_layer.remove_all_contacts()"
remove_contacts_hash="            #self.data_layer.remove_all_contacts()"

find $path -name $filename | while read line;
do
    sed -i "/^$remove_contacts/ c\\$remove_contacts_hash" $line
done