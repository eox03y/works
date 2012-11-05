#!/usr/bin/env python
# -*- coding: EUC-KR -*-
#
import html2txt
from urllib import urlopen
import re

URL = "http://hometopia.com/proverb/prov-e1a.html"

SAMPLE = """\
"""

def save():
	pass

def get_prov_list(html):
	p1 = html.find("<ol>")
	p2 = html.find("</ol>", p1)
	if p1!=-1 and p2!=-1:
		return html[p1:p2]
	else:
		return ''

	
def process(txt, out):
	lines = txt.split('\n')
	
	n = 0
	hangul = 0
	comment = 0
	while n < len(lines):
		l = lines[n].strip()
		if len(l)==0 or l[0].isspace(): 
			n += 1
			continue

		if l[0].isalpha():
			if hangul==1: out.write("\n")
			hangul = 0
			comment = 0
			out.write("%s\n" % l)

		if ord(l[0]) > 128 and comment != 1:
			if hangul==0: out.write("\n")
			hangul = 1
			out.write("%s\n" % l)

		if l[0]=="-":
			comment = 1
	
		n += 1

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
		url = "http://hometopia.com/proverb/prov-e1%c.html" % number
		print url
		html = fetchurl(url)
		if html != "":
			try:
				part = get_prov_list(html)

				h2t = html2txt.html2txt(url)
				h2t.feed(part)
				process( h2t.data, out)
			except:
				print "failed "
				raise
		

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

