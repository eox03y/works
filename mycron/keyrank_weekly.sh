#!/bin/bash

if [ $1 $2 ]
then
LASTWEEK=$1
YESTERDAY=$2
else
LASTWEEK=`date --date='1 week ago' +%Y-%m-%d`
YESTERDAY=`TZ=GMT+24 date +%Y-%m-%d`
YESTERDAY=`date --date='1 day ago' +%Y-%m-%d`
fi
echo $LASTWEEK $YESTERDAY 
cd ~/bin
python ~/bin/queryKeywordRankExcel.py LHRHVH $LASTWEEK $YESTERDAY >> stat.log
python ~/bin/queryKeywordRankExcel.py APPS $LASTWEEK $YESTERDAY >> stat.log
