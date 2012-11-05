#!/usr/bin/env python
# -*- coding: euc-kr -*-

import urllib2
from BeautifulSoup import BeautifulSoup

dict = {}
Topurl = ['/News_and_Media', '/Computers_and_Internet','/Recreation','/Business_and_Economy', '/entertainment', '/Education', '/Health', '/Society_and_Culture', '/Government', '/Arts', '/Science', '/Humanities__Social_Science', '/Regional', '/Reference']

# dictionary prototype level 1 -> 

def do_it():
	#while dict.keys() != []:
	while True:
		if len(Topurl) == 0:
			break

		url = 'http://kr.dir.yahoo.com'
		trv = Topurl.pop()
		fp = open(trv[1:] + '.html', 'w')

		url = url + trv

		req = urllib2.Request(url)
		response = urllib2.urlopen(req)

		fp.write(response.read())
		fp.close()
	
def example():
	page = urllib2.urlopen("http://kr.dir.yahoo.com")
	#page = urllib2.urlopen("http://kr.dir.yahoo.com/News_and_Media/")
	#page = urllib2.urlopen("http://kr.dir.yahoo.com/News_and_Media/Newspapers/")
	page = urllib2.urlopen("http://kr.dir.yahoo.com/Society_and_Culture/")

	#soup = BeautifulSoup(page)

	#print soup.prettify()
	print page.read()
	#tag = soup.a
	#tag = soup.findAll('a')

	#print tag[1]['href']

	# prettify 해준다음에 html 을 끊어서 � 다시 a tag 를 찾는다.

	#for i in tag:
		##print i.renderContents()
		#print i.prettify()

	#print tag.renderContents()
	#for incident in soup('a',):
		#where, linebreak, what = incident.contents[:3]
		#print where.strip()
		#print what.strip()
		#print

if __name__ == '__main__':
	do_it()
	#example()
