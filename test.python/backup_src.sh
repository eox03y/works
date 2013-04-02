#STR=`date --date="1 day ago" +"%Y-%m-%d"`
STR=`date +"%Y-%m-%d"-%H`
echo $STR
F=all_py.$STR.tar
tar cf $F *.py *.sh
#s3cmd put $F s3://sch-emr/handol/$F
bash s3put.sh $F
