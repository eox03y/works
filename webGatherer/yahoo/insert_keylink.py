#!/usr/bin/python
# -*- coding: utf-8 -*-

###################################################
# Sproject
# 야후에서 수집한 URL 들의 키워드와 타이틀을 구하여 화일저장한다.
# URL 중 복잡한 것은 제외.
# 같은 도멘인은 한 개의 URL 만 처리.
# 2007.06.27 handol@gmail.com
#
###################################################

import sys
import MySQLdb


def logindb(dbname):
	try:
		db = MySQLdb.connect(host="localhost", user="root", passwd="wpxk00", db=dbname)
		db.set_character_set('utf8')
		return db

	except MySQLdb.OperationalError, message:
		errorMessage = "error %d:\n%s" % (message[0], message[1])
		print errorMessage
		return 


def insert_keyword(db, keyword, url):
	print url
	cursor = db.cursor()
	#user_i에 0은 입력 안됨.
	#cmd = "insert into submiturls (user_id, url, description, keyword) values (14, '%s', '%s', '%s')" % ( url, keyword, keyword)
	cmd = "insert into submiturls (user_id, url, description, keyword) values (14, 'http://anydict.com', 'anydic', 'anydic')"
	cursor.execute(cmd)
	db.commit()
	print "insert= ", cursor.rowcount
	print "lastrowid= ", cursor.lastrowid
	print "db result = ", cursor.messages
	cursor.close()


def doit(db):
	fp = open("a", "r")
	cnt = 0
	while 1:
		line = fp.readline()
		if line==None or line=="":
			break

		if line.startswith("=="):
			continue

		url = line.strip()
		keyword = fp.readline().strip()

		insert_keyword(db, keyword, url)

		cnt += 1

		if cnt > 5:
			break
		


if __name__ == '__main__':
	db = logindb('keylink')
	doit(db)
