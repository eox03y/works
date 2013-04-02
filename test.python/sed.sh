for i in qc_log*.csv;
do
echo $i
sed 's/\t/ , /g' $i  > /tmp/handol.t
/bin/cp /tmp/handol.t $i
done

tar cvf qc_log.all.tar qc_log.*.csv
gzip qc_log.all.tar
python handol_s3_put.py qc_log.all.tar.gz  qc_log.all.tar.gz

