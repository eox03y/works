#!/bin/bash
if [ $# -ge 2 ] 
then
echo $1 $2/$1
python ~/bin/s3_cmd.py $1 $2/$1
fi

