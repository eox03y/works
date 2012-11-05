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
import urlparse

import BeautifulSoup

import codecs

DOMAIN_LIST = {}

def isGoodUrl(url):
	if url.find('?') != -1:
		return 0
	if url.find('~') != -1:
		return 0

	scheme, host, path, params, query, fragment = urlparse.urlparse(url)

	if query != '':
		return 0

	if len(path) > 1:
		return 0

	if path.count('/') > 2:
		return 0

	if DOMAIN_LIST.has_key(host):
		return 0
	else:
		DOMAIN_LIST[host] = 1
		return 1


def clean_keyword(keyword):
	pos = keyword.find('(')
	if pos != -1:
		keyword = keyword[:pos]

	pos = keyword.find(',')
	if pos != -1:
		keyword = keyword[:pos]

	return keyword

def logindb(dbname):
	try:
		db = MySQLdb.connect(host="localhost", user="root", passwd="wpxk00", db=dbname)
		db.set_character_set('utf8')
		return db

	except MySQLdb.OperationalError, message:
		errorMessage = "error %d:\n%s" % (message[0], message[1])
		print errorMessage
		return 


def print_keylink(db):
	cursor = db.cursor()
	cmd = "select id, user_id, url from submiturls"
	cursor.execute(cmd)
	result = cursor.fetchall()
	for res in result:
		#print res[0],res[2] 
		pass
	cursor.close()


def insert_keyword(db, keyword, url):
	cursor = db.cursor()
	#user_i에 0은 입력 안됨.
	cmd = "insert into submiturls (user_id, url, description, keyword, created_at) values (14, '%s', '%s', '%s', now())" % ( url, keyword, keyword)
	cursor.execute(cmd)
	db.commit()
	cursor.close()

def yahoo_list(db, id):
	#out = open("keylink.txt", "a+")
	try:
		out = codecs.open("keylink.txt", encoding='utf-8', mode='a+')
	except:
		return -1

	try:
		cursor = db.cursor()
		cmd = "select * from url where id >= %d" % (id)
		cursor.execute(cmd)

	except MySQLdb.OperationalError, message:
		errorMessage = "error %d:\n%s" % (message[0], message[1])
		print errorMessage
		return

	else:
		result = cursor.fetchall()
		cursor.close()
		db.close()

		print db
		db2 = logindb("keylink")
		print db2

		print type(result)

		cnt = 0

		for record in result:
			id = record[0]
			url = record[4]
			#keyword = conv_utf8_to_euckr(record[2])
			keyword = record[2]
			#print "keyword=", type(keyword)

			desc = record[3]
			if isGoodUrl(url)==0:
				continue
			out.write("== %d\n" % id)
			#print ("== %d" % id)

			try:
				out.write("%s\n" % url)
			except:
				#print url
				pass
			#print url

			#out.write("%s\n" % record[2])
			#print ("%s" % record[2])

			keyword = clean_keyword(keyword)
			insert_keyword(db2, keyword, url)
			
			cnt += 1

			continue
			try:
				title = fetchUrl(url)
			except:
				title = keyword

			#out.write("%s\n" % keyword)
			#out.write("%s\n" % title)
			out.write("\n")



def conv_utf8_to_euckr(utfstr):
	#print utfstr.__str__()
	#print "utfstr=", type(utfstr)
	#return utfstr.decode('utf-8').encode('euc-kr')
	return utfstr.decode('utf-8')



import urllib

urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')

def fetchUrl(urlstr):
	print urlstr
	fp = urllib.urlopen(urlstr)
	html = fp.read()
	#print dir(fp.headers)
	contentType = fp.headers.getheader('content-type')
	#print contentType
	charset = getCharset(contentType)
	charset = charset.lower()
	print charset
	
	if charset=="":
		charset='euc-kr'
	#print len(html)
	soup = BeautifulSoup.BeautifulSoup(html, fromEncoding=charset)
	for title in soup('title'):
		#print title
		#print dir(title)
		#print title.contents[0]
		if title==None:
			return ""

		if charset=='utf-8' or charset=='utf8':
			print conv_utf8_to_euckr(title.contents[0])
			return  conv_utf8_to_euckr(title.contents[0])
		else:
			print title.contents[0]
			return title.contents[0]
		break
	print

def getCharset(header):
	pos = header.find("charset")
	if pos==-1:
		return ""

	pos = header.find("=", pos)
	if pos==-1:
		return ""

	pos2 = header.find("\n", pos)
	if  pos2==-1:
		return header[pos+1:]
	else:
		return header[pos+1:pos2]	

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage: start_id'
		sys.exit(0)

	#fetchUrl("http://www.naver.com")
	fetchUrl("http://www.me2day.net")
	db = logindb('categorydb')
	yahoo_list(db, int(sys.argv[1]))
