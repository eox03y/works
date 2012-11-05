#!/usr/bin/env python
# -*- coding: EUC-KR -*-

import os
from hangul import findhanchar

def all_engdic(dictpath, start, end):
	for alpha in range(ord(start), ord(end)+1):
		print chr(alpha)
		fname = os.path.join(dictpath, chr(alpha) + ".dic")
		proc_engdic(fname)

def proc_engdic(fname):
	try:
		fd = open(fname, 'r')
	except:
		print "reading failed:", fname

	try:
		out = open(fname+".good", 'w')
		pass
	except:
		print "writing failed:", fname

	n = 0
	for line in fd.xreadlines():
		#line = line.strip()
		p = line.find(":")

		if p == -1:
			print line
			line = repairline(line)
			print line
		out.write(line)


def repairline(line):
	p1 = line.find('[')
	if p1 == -1: return ''
	
	p3 = line.find('=', p1+1)
	if p3 != -1 and line[p3+1].isupper():
		p2 = p3+1
	else:
		p2 = findhanchar(line, p1+1)
		if p2 == -1: 
			return ''

		if line[p2-1] == '(':
			p2 -= 1

	return "%s : %s" % (line[:p1] , line[p2:])

		

if __name__ == "__main__":
	if os.getenv("SHELL") != None:
		hdic = all_engdic("/data1/AD/data/engdic/", 'a','z')
	else:
		hdic = all_engdic("C:/Works/ad_svc_backup/ad_svc_data/engdic/", 'a','z')
