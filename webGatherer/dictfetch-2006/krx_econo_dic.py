#!/usr/bin/env python
# -*- coding: EUC-KR -*-
#
import html2txt
from urllib import urlopen


URL = "http://sm.krx.co.kr/common/dictionary/kse_voca_body.jsp?dic_seq_no=18"

URL_RANGE = "1~13098"

SAMPLE = """\
KRX증권용어사전
옵션부 사채
(
Bond with imbedded option
)
옵션부사채(BO)란 채권 발행시 제시되는 일정 조건이 성립되면 만기 전이라도 발행회사는 사채권자에게 매도청구(call option)를, 사채권자는 발행회사에 상환청구(put option)를 할 수 있는 권리가 부여된 새로운 채권이다.

"""

def save():
	pass

def process(txt, out):
	lines = txt.split('\n')

	#for l in lines:
	#	print l

	head = lines[1].strip()
	second = lines[3].strip()
	expl = ' '.join( lines[5:] )
	expl = expl.strip()

	if head == '': return

	print head

	out.write("@@0 %s\n" % head)
	if second != '': 
		out.write("@@1 %s\n" % second)
	if expl != '': 
		out.write("$$ %s\n" % expl)
	out.write('\n')
	
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
		url = "http://sm.krx.co.kr/common/dictionary/kse_voca_body.jsp?dic_seq_no=%s" % number
		html = fetchurl(url)
		if html != "":
			try:
				h2t = html2txt.html2txt(url)
				h2t.feed(html)
				process(h2t.data, out)
			except:
				print "fail for number : %d" % number
		

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 4:
		print "usage: %s from to outfile" % sys.argv[0]
		sys.exit(0)


	try:
		out = open(sys.argv[3], "w+")
		main (int(sys.argv[1]), int(sys.argv[2]), out)	
	except:
		print "cannot write outfile", sys.argv[3]

