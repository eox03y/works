#!/usr/bin/env python
# -*- coding: EUC-KR -*-
#
# 무역 용어 (영어) 표제어 목록 추출 
# A~Z
# http://www.kita.net/dictionary/n_trade_dic.jsp?keyword=A&mode=2&top_menu_id=db31

import sys
import re
import html2txt
from urllib import urlopen


RANGE = range(ord('A'),ord('Z')+1)


SAMPLE_TXT = \
"""
무역용어사전
A.T.A(Admission Temporaire- Temporary Admission)
A.T.A협약
물품의 일시면세수입에 관한 절차를 용이하게 하기 위하여 물품의 일시수입에 관한 공통된 절차를 규정한 관세협약(1961.12.6 브뤼셀에서 채택)으로 통상협약에 의하여 발급된 일시수입통관증서를 A.T.A Carnet라 한다.
"""


def process(txt, out, url=''):
	lines = txt.split('\n')

	#for l in lines:
	#	print l

	head = lines[2].strip()
	second = lines[3].strip()
	expl = '\n'.join( lines[5:] )
	expl = expl.strip()

	if head == '': return

	print head

	if url != '':
		out.write("## %s\n" % url)

	out.write("@@0 %s\n" % head)
	if second != '': 
		out.write("@@1 %s\n" % second)
	if expl != '': 
		out.write("$$ %s $$\n" % expl)
	out.write('\n')
	out.flush()
	
def getdict(paras, out):
	url = "http://www.kita.net/dictionary/view_dic.jsp?mode=%s&keyword=%s&seq_no=%s" % (paras[0], paras[1], paras[2])

	html = fetchurl(url)
	if html == "": 
		print "fetch fail:", url
		return

	try:
		h2t = html2txt.html2txt(url)
		h2t.feed(html)
	except:
		return

	#print h2t.data
	process(h2t.data, out, url)
	#sys.exit(0)
	pass

def mystrip(str):
	return str.strip().strip("'")

def idx(htmlline, out):
	p = re.compile(r'\((.+)\)')
	s = p.search(htmlline)
	if s != None:
		#print s.group(0)

		paras = s.group(0)[1:-1]

		paras = paras.split(',')
		pp = map(mystrip, paras)

		getdict(pp, out)

		#print ' '.join(pp)
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
			
			idx(html[pos+offset:pos+offset+128], out)
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

