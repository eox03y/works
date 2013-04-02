#!/bin/bash

#STR=`date --date="1 day ago" +"%Y-%m-%d"`

LOG='qc_log_all.UK.log'
touch $LOG
python analyze_main_UK.py 2013-01-01 2013-02-01

