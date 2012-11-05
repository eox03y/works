#!/usr/bin/env python
# -*- coding: EUC-KR -*-
#
# 경제 용어 (한글) 표제어 목록 추출
# 1~14
# url = "http://sm.krx.co.kr//common/dictionary/kse_voca_left.jsp?language=Korean&dic_typ=A001&code=%02d" % number

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

def idx(anchors, out):
	
	for url,ref in anchors:	
		#num = int(url[-2:])
		#out.write("%d\n" % num)		
		out.write("%s\n" % url)		
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
		url = "http://sm.krx.co.kr//common/dictionary/kse_voca_left.jsp?language=Korean&dic_typ=A001&code=%02d" % number
		html = fetchurl(url)
		if html != "":
			try:
				h2t = html2txt.html2txt(url)
				h2t.feed(html)
				idx(h2t.anchors, out)
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

