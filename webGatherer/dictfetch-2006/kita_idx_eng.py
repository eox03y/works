#!/usr/bin/env python
# -*- coding: EUC-KR -*-
#
# 무역 용어 (영어) 표제어 목록 추출 
# A~Z
# http://www.kita.net/dictionary/n_trade_dic.jsp?keyword=A&mode=2&top_menu_id=db31

import re
#import html2txt
from urllib import urlopen


RANGE = range(ord('A'),ord('Z')+1)


def save():
	pass

def mystrip(str):
	return str.strip().strip("'")

def idx(htmlline):
	p = re.compile(r'\((.+)\)')
	s = p.search(htmlline)
	if s != None:
		#print s.group(0)

		paras = s.group(0)[1:-1]
		out.write("%s\n" % paras)		

		paras = paras.split(',')
		pp = map(mystrip, paras[:3])
		print ' '.join(pp)
	pass


def fetchurl(url):
	try:
		doc = urlopen(url).read()
		return doc
	except:
		print "fetch failed for ", url
		return ""

def main(fromnum, tonum, out):
	for number in range(fromnum, tonum+1):
		print number
		url = "http://www.kita.net/dictionary/n_trade_dic.jsp?keyword=%c&mode=2&top_menu_id=db31" % number 
		html = fetchurl(url)
		if html == "":
			print "failed : ", url
			return

		target = "javascript:viewDictionary"

		pos = 0
		while 1:	
			offset = html[pos:].find(target)
			if offset == -1: break
			
			idx(html[pos+offset:pos+offset+128])
			pos = pos + offset + len(target)


if __name__ == "__main__":
	import sys
	if len(sys.argv) < 4:
		print "usage: %s from to outfile" % sys.argv[0]
		sys.exit(0)


	try:
		out = open(sys.argv[3], "w+")
	except:
		print "cannot write outfile", sys.argv[3]

	main (ord(sys.argv[1][0]), ord(sys.argv[2][0]), out)	

