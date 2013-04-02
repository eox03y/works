#!/usr/bin/python

import sys
import re


def divider(row,dt_map):
	key,value = row.split('=')
	
	if value == 'null':
		value = ''
	
	dt_map[key] = value.strip()
	

def setter(row):
	
	dt_map = {}
	
	for temp in row.split('|@'):
		divider(temp, dt_map)
		
	if dt_map['si'] == '0':
		dt_map['mct'] = 0
	else:
		dt_map['mct'] = 1
	
	printFormat(dt_map)

def printFormat(dt_map):
	
	print  dt_map['sn'] + "|" + dt_map['dos'] +"|" + dt_map['dm'] + "\t1" +"\t"+dt_map['tot'] +"\t"+ str(dt_map['mct'])
	print  dt_map['sn'] + "|" + 'all' +"|" + dt_map['dm'] + "\t1" +"\t"+dt_map['tot'] +"\t"+ str(dt_map['mct'])
	print  dt_map['sn'] + "|" + dt_map['dos'] +"|" + 'all' + "\t1" +"\t"+dt_map['tot'] +"\t"+ str(dt_map['mct'])
	
	

	
def main(argv):
        
		
		#f = open("osp_query.log")
		line = sys.stdin.readline()
		#line = f.readline()
		
		
		
		while line:
			
			pattern = line.split("|", 1)
			setter(pattern[1])
			line = sys.stdin.readline()
			#line = f.readline()
			
if __name__ == "__main__":
        main(sys.argv)
