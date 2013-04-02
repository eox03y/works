#!/usr/bin/python

import sys
import re


#13-11-2012 00:00:18:198|test0astor|$|test0astorusa01|$|Android 4|$|GT-P5113|$|super mario bros. game|$|54

def divider(row,dt_map):
	key,value = row.split('=')
	
	if value == 'null':
		value = ''
	
	dt_map[key] = value.strip()
	

def setter(row):
	
	
	dt_map = {}
	
	
	
	
	line = row.split('|')

	if len(line) == 12:
		dt_map['sn'] = line[3]
		dt_map['dos'] = line[5]
		dt_map['dm'] = line[7]
		dt_map['q'] = line[9]
		dt_map['tot'] = line[11]
		dt_map['mct']= "0"
		if dt_map['q'] == '카카오톡'
			printFormat(dt_map)

def printFormat(dt_map):
	
	print  dt_map['sn'] + "|" + 'all' +"|" + 'all' + "|"+ dt_map['q'] + "\t" + "1" +"\t"+ dt_map['tot'].strip() + "\t" + dt_map['mct'].strip()
	print  dt_map['sn'] + "|" + 'all' +"|" + dt_map['dm'] + "|"+ dt_map['q'] +"\t"+ "1" +"\t" + dt_map['tot'].strip() + "\t" + dt_map['mct'].strip()
	print  dt_map['sn'] + "|" + dt_map['dos'] +"|" + 'all' + "|"+ dt_map['q'] + "\t" + "1" +"\t"+dt_map['tot'].strip() +"\t"+ dt_map['mct'].strip()
	
	

	
def main(argv):
        
		
		#f = open("osp_query.log")
		line = sys.stdin.readline()
		#line = f.readline()
		
		
		
		while line:
			
			
			setter(line)
			line = sys.stdin.readline()
			#line = f.readline()
			
if __name__ == "__main__":
        main(sys.argv)
