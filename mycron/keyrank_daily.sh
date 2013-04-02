#!/bin/bash

if [ $1 ]
then
YESTERDAY=$1
else
YESTERDAY=`TZ=GMT+24 date +%Y-%m-%d`
YESTERDAY=`date --date='1 day ago' +%Y-%m-%d`
LASTWEEK=`date --date='1 week ago' +%Y-%m-%d`
fi

cd ~/bin
python ~/bin/queryKeywordRankExcel.py LHRHVH $YESTERDAY $YESTERDAY >> stat.log
python ~/bin/queryKeywordRankExcel.py APPS $YESTERDAY $YESTERDAY >> stat.log
