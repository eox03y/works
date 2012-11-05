import BeautifulSoup
import re
import codecs

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
	return html, charset

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


def readfile(fname):
	try:
		fp = open(fname)
	except:
		print "reading failed", fname
		return

	html = fp.read()
	fp.close()
	charset='euc-kr'

	return html, charset


def rankey(html, charset):

	print "####", len(html)
	soup = BeautifulSoup.BeautifulSoup(html, fromEncoding=charset)


	#for title in soup('title'):
	#	print title

	out = codecs.open("out.txt", encoding='euc-kr', mode='a+')


	for a in soup.findAll('a', href=re.compile('^http://redirect.rankey.com/redirect.html')):
		#print a.href
		linkurl = a['href']
		mark = 'http%3A%2F%2F'
		pos = linkurl.find(mark)
		if pos == -1: 
			continue
		linkurl = linkurl[pos+len(mark):]
		linkname = a['title']

		out.write("%s\t%s\n" % (linkurl, linkname))

	out.close()
	print

def do_by_file(fname):
	html, charset = readfile(fname)
	rankey(html, charset)

def do_by_url():
	for i in range(8):
		url = "http://rankey.com/rank/top200.php?l_rank_year=2007&l_rank_month=07&l_rank_week=02&gubun=&sort=V_RANKING&order=ASC&select_rank=m3&page=%d" % (i+1)

		html, charset = fetchUrl(url)
		rankey(html, charset)



import sys

if len(sys.argv) < 2:
	print "%s html_file" % (sys.argv[0])
	sys.exit()


#do_by_file(sys.argv[1])
do_by_url()

