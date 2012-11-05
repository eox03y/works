#!/usr/bin/python
# -*- coding: euckr -*-

###################################################
# Sproject
# Category result to DB
# 2007.5.22 by GuyBrush
#
###################################################

import sys
import MySQLdb

url_table = {}
db_data = {}

def getinfowebsite(inputfile):
	fp = open(inputfile, 'r')
	
	catenum = 0
	sitename = ''
	desc = ''
	urls = ''

	content = fp.read()
	content = content.split('\n')

	linenum = 1
	counter = 1

	#print '*' * 12
	#print content[0:10]
	#print '*' * 12

	# Let's make Intelligent Robot w c make a dicision

	for line in content:
		if line == '--begin--':
			catenum = content[ linenum ]
			counter = 1
		elif line == '--end--':
			pass

		elif counter % 3 == 0:
			sitename = content[ linenum - 1 ]
			desc = content[ linenum + 0 ]
			if desc.find('http') != -1:
				urls = desc
				desc = ''
				counter += 1
			else:
				urls = content[ linenum + 1 ]
			# calll db input function
			#print 'cate:', catenum
			#print 'site:', sitename
			#print 'desc:', desc
			#print 'urls:', urls
			#print '-' * 15
			input_mysql((catenum, sitename, desc, urls))

		linenum += 1
		counter += 1

		#print linenum, counter

	fp.close()
	return 1

def read_url_table():
	fp = open('urltable.txt', 'r')
	for line in fp:
		line = line.split()
		# real category name splited '/'
		# but the name duplicated. so we use full category name

		url_table[line[1].strip("'")] = line[0]
	
	# This is For TEST
	#for i in url_table:
		#print i,':',url_table[i]
	#cname = '/Computers_and_Internet/Desktop_Publishing'
	#print url_table[cname]
	fp.close()
	return 1
		
def getinfocategory(inputfile):
	fp = open(inputfile, 'r')

	content = fp.read()
	content = content.split('\n')


	linenum = 1
	for line in content:
		# each category line begins with '/'
		if line.find('/') != -1: 
			splited = line.split('/')
			name = splited[-1]
			#parent_name = splited[-2]	# can cause prob.
			hname = content [ linenum ]

			id = url_table.get(line)
			inx = line.rfind(name)
			parentfullname = line[ : inx -1 ]
			parent_num = url_table.get(parentfullname, '-1')
			#print name, parent_name, hname
			if id == None:
				print 'id not exist urltable', line
			else:
				#print 'called', id, name, hname, parent_num
				input_cate_mysql((id, name, hname, parent_num))

		linenum += 1

		########### TEST ###########
		#if linenum == 300:
			#break

		#print linenum, counter

	fp.close()
	return 

def input_cate_mysql(input):
	try:

		db = MySQLdb.connect(host="localhost", user="root", passwd="wpxk00", db="categorydb")
		db.set_character_set('utf8')
		cursor = db.cursor()
		#cursor.execute("select * from dict_1 limit 0,10 ")
		#cursor.execute("desc category")
		#cmd = "insert into dict_1 (eword, hword, meaning) values (" + input[0] + ',' + input[1] + ',' + input[2] + ")"
		#caid,sitename, desc, urls = input

		id, name, mean, parent_num = input

		#print type(id), type(name), type(mean), type(parent_num)


		cmd = "insert into catetable(id, name, mean, parent_1 ) values('" + id + "','" + name + "','" + mean + "','" + parent_num + "')"
		cursor.execute(cmd)

	except MySQLdb.OperationalError, message:
		errorMessage = "error %d:\n%s" % (message[0], message[1])
		print errorMessage
		return

	except:
		fe = open('error.log', 'a')
		fe.write(id + name+' ' + mean + repr(parent_num) + '\n')
		#fe.write(hword+'\n')
		#fe.write(eword+'\n')
		#fe.write(meaning+'\n')
		fe.write('----\n')
		fe.close()
		return
	else:
		result = cursor.fetchall()
		fields = cursor.description

		#for record in result:
			#print record[0] , "-->", record[1], "**>",record[2]
		cursor.close()
		db.close()

def input_mysql(input):

		
	try:
		db = MySQLdb.connect(host="localhost", user="root", passwd="wpxk00", db="categorydb")
		db.set_character_set('utf8')
		cursor = db.cursor()
		#cursor.execute("select * from dict_1 limit 0,10 ")
		#cursor.execute("desc category")
		#cmd = "insert into dict_1 (eword, hword, meaning) values (" + input[0] + ',' + input[1] + ',' + input[2] + ")"
		caid,sitename, desc, urls = input

		cmd = "insert into url(category_id, sitename, description, urls ) values('" + caid + "','" + sitename + "','" + desc + "','" +urls+"')"
		#print cmd
		cursor.execute(cmd)

	except MySQLdb.OperationalError, message:
		errorMessage = "error %d:\n%s" % (message[0], message[1])
		return

	except:
		fe = open('error.log', 'a')
		fe.write(sitename+'\n')
		#fe.write(hword+'\n')
		#fe.write(eword+'\n')
		#fe.write(meaning+'\n')
		fe.write('----')
		fe.close()
		return
	else:
		result = cursor.fetchall()
		fields = cursor.description

		#for record in result:
			#print record[0] , "-->", record[1], "**>",record[2]
		cursor.close()
		db.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'argument error: executefile.py textfile'
		sys.exit(0)
	# if U wanna input urlwebsite: getinfowebsite
	# if U wanna input category: read_url_table, getinfocategory
	getinfowebsite(sys.argv[1])
	#read_url_table()
	#getinfocategory(sys.argv[1])

	
