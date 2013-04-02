#!/bin/bash

#STR=`date --date="1 day ago" +"%Y-%m-%d"`

LOG='qc_log_one.log'
touch $LOG
python analyze_main.py 2013-01-31 2013-01-31 >> $LOG

