#!/usr/bin/env python
# -*- coding: EUC-KR -*-
#
import time
print time.tzname 
import html2txt
from urllib import urlopen
import re

g_StartTime = 0

def delete_tag(txt):
	p1 = txt.find("<")

	while p1 != -1:
		p2 = txt.find(">")
		txt=txt.replace(txt[p1:p2+1],"")
		p1 = txt.find("<")
	pass

	return txt
	
def process(txt, out):
	hword_start = "<P><B><FONT FACE=\"바탕\">"
	hword_end = "</B>"

	p1 = txt.find(hword_start)
	txt = txt[p1+len(hword_start):]
	
	while p1 != -1:
		p1 = txt.find(hword_start)
		save_txt = txt[:p1]

		p2 = save_txt.rfind(hword_end)
		hword = save_txt[:p2]
		des = save_txt[p2+len(hword_end):]

		hword = delete_tag(hword)
		des = delete_tag(des)
	 	des = des.replace("\r","")

		out.write("%s\n" %hword)
		out.write("%s\n" %des)

		txt = txt[p1+len(hword_start):]
	pass

def fetchurl(url):
	try:
		doc = urlopen(url).read()
		return doc
	except:
		print "fetch failed for ", url
		return ""

def main(fromnum, tonum, out):
	g_StartTime = time.time()
	
	for number in range(fromnum, tonum+1):
	#for number in range(u"ㄱ",u"ㅁ"):
		url = "http://www.poomzil.co.kr/건설용어사전/%c.htm" % number
		print url

		html = fetchurl(url)
		if html != "":
			try:
				process( html, out)
			except:
				print "failed "
				raise
	elapsedTime = time.time()-g_StartTime
	print "Elapsed time : %d seconds" % elapsedTime
	#print "%d" % int(u'ㄲ')

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 4:
		print "usage: %s from to outfile" % sys.argv[0]
		sys.exit(0)


	try:
		out = open(sys.argv[3], "w+")
		main (ord(sys.argv[1]), ord(sys.argv[2]), out)	
	except:
		print "cannot write outfile", sys.argv[3]
		raise

