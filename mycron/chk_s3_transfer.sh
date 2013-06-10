#!/bin/bash

if [ $1 ]
then
YESTERDAY=$1
else
YESTERDAY=`TZ=GMT+24 date +%Y%m%d`
fi

python /home/search/handol/mypy_tools/mycron/chk_s3_transfer.py $YESTERDAY MAIL
