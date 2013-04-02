#!/bin/bash

#STR=`date --date="1 day ago" +"%Y-%m-%d"`

LOG='qc_log_all.2.log'
touch $LOG
python analyze_main.py 2012-12-25 2013-02-01 >> $LOG

