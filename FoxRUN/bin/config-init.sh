#!/bin/bash
#add the parmater from user input into config file, "manifest.ini" and "mtbf.list","ApplicationList.ini"
app_name=$1
path=$2

webapp_path=$path"/pythontests/webapptest"


suffix=".py"
prefix="test_"
declare applist=""


if [ $app_name = "all" ]
then
    index=0

    while read line
    do
        if [[ $line =~ ^[A-Za-z_]+$ ]];
        then
            applist=$applist' '$line
            index=$((index+1))

        fi
    done <$path"/ApplicationList.ini"
else
    sed -i '/^[a-z]/d' $path"/ApplicationList.ini"

    applist=${app_name//','/' '}
fi

#modify "mtbf.list" dir
find $webapp_path -name "*.list" | while read line;
do
    #delete last two line, that is "}"and "]"
    sed -i 'N;$!P;$!D;$d' $line

    sed '/\"test_/d' -i $line

    for app in $applist;
    do
        grep -q '"'$prefix$app$suffix'"' $line ||
        {
            echo '"'$prefix$app$suffix'",' >>$line
        }
    done

    #delete last ","
    sed -i '$s/.$//' $line

    #add last two line, that is "}"and "]"
    echo -e "]"  >>$line
    echo -e "}"  >>$line
done

#modify "manifest.ini" at "webapptest" dir
find $webapp_path -name "*.ini" | while read line;
do
    sed '/\[test_/d' -i $line

    for app in $applist;
    do
        grep -q '\['$prefix$app$suffix'\]' $line ||
        {
            echo '['$prefix$app$suffix']' >> $line
        }
    done
done


#modify "ApplicationList.ini" at "avetest" dir
find $path -name "ApplicationList.ini" | while read line;
do
    for app in $applist;
    do
        grep -q $app $line ||
        {
            echo $app >>$line
        }
    done
done


