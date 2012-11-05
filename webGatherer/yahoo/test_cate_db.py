#!/usr/bin/python
# -*- coding: euckr -*-

###################################################
# Sproject
# Test Category DB
# 2007.06.27 handol@gmail.com
#
###################################################

import sys
import MySQLdb

def logindb():
	try:
		db = MySQLdb.connect(host="localhost", user="root", passwd="wpxk00", db="categorydb")
		db.set_character_set('utf8')
		return db

	except MySQLdb.OperationalError, message:
		errorMessage = "error %d:\n%s" % (message[0], message[1])
		print errorMessage
		return 

def checkctg(db, id):
	try:
		cursor = db.cursor()
		cmd = "select * from catetable where id=%d" % (id)
		cursor.execute(cmd)

	except MySQLdb.OperationalError, message:
		errorMessage = "error %d:\n%s" % (message[0], message[1])
		print errorMessage
		return

	else:
		#result = cursor.fetchall()
		result = cursor.fetchone()
		#fields = cursor.description

		record = result
		#print record[0] , "-->", record[1], record[2], record[3], record[4]
		print "Ctg: ",record[0]
		print "\tparent: ",record[3], record[4], record[5]
		print "\t", conv_utf8_to_euckr(record[1])
		print "\t", conv_utf8_to_euckr(record[2])
	cursor.close()

def checkurl(db, id):
	try:
		cursor = db.cursor()
		cmd = "select * from url where id=%d" % (id)
		cursor.execute(cmd)

	except MySQLdb.OperationalError, message:
		errorMessage = "error %d:\n%s" % (message[0], message[1])
		print errorMessage
		return

	else:
		#result = cursor.fetchall()
		result = cursor.fetchone()
		#fields = cursor.description

		record = result
		#print record[0] , "-->", record[1], record[2], record[3], record[4]
		print record[0] , "--> ", record[1]
		print "\t", conv_utf8_to_euckr(record[2])
		print "\t", conv_utf8_to_euckr(record[3])
		print "\t", conv_utf8_to_euckr(record[4])
		cursor.close()

		checkctg(db, record[1])

def conv_utf8_to_euckr(str):
	return str.decode('utf-8').encode('euc-kr')


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage: category_id'
		sys.exit(0)

	db = logindb()
	checkurl(db, int(sys.argv[1]))
	db.close()
