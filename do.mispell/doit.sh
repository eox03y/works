#!/bin/bash
for orgf in pagecounts-20130301-*0000.gz;
do
	b=`basename $orgf .gz`
	echo $b
	gzip -dc $orgf | grep "^en " | python en_filter.py | gzip -cf > $b.en.gz
done
	

merged=all.en.gz
tmp=tmp.en.gz
touch $merged
for enf in pagecounts-20130301-*0000.en.gz;
do
	echo $enf
	python merge_key_int_value.py $merged $enf $tmp 
	/bin/cp $tmp $merged
done
