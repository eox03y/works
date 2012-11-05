#!/usr/bin/env python
# -*- coding: euc-kr -*-
import urllib
import urlparse
import httplib
import urllib2

import BeautifulSoup

#httplib.HTTPConnection.debuglevel = 1 

urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')

def fetchurl_1(urlstr, debug=0):
	fp = urllib.urlopen(urlstr)
	html = fp.read()
	if debug: print fp.headers
	if debug: print len(html)
	return html

def fetchurl_2(urlstr):
	request = urllib2.Request(urlstr)
	opener = urllib2.build_opener()
	f = opener.open(request)
	#print f.status
	print f.url

def getHEAD(urlstr):
	urlfields = urlparse.urlparse(urlstr)
	host = urlfields[1]
	path = "".join(urlfields[2:])
	#path = "".join(list(urlfields[2:]))
	#print "Host = %s" % (host)
	#print "path = %s" % (path)
	conn = httplib.HTTPConnection(host)
	conn.request("HEAD", path)
	r2 = conn.getresponse()
	#print r2.getheaders()
	print r2.getheader('location')


def get_text(htmltree):
	text = ""
	for item in htmltree:

		#print item, item.__class__.__name__
		if item.__class__.__name__ == "Tag":
			text += get_text(item)
		else:
			text += item
	return text


def saveLink(soup, tagname, out):
	for link in soup(tagname):
		#print link
		try:
			out.write(link['href'])
			out.write('\t')
		except:
			continue

		#print link.contents
		try:
			link_name = get_text(link.contents)
			link_name = link_name.strip()
			#print link_name
			out.write(link_name)
			out.write('\n')
		except:
			pass


class trimLines:
	def __init__(self):
		self.cnt = 0
		self.prevEmpty = False

	def filter(self, line):
		isThisGoodLine = True
		t = line.strip()
		if len(t) == 0:
			if self.prevEmpty:
				isThisGoodLine = False		
			self.prevEmpty = True
		else:
			self.prevEmpty = False
		return isThisGoodLine
		
def getOnlyText(soup):
	#getting all comments 
	comments = soup.findAll(text=lambda text:isinstance(text, BeautifulSoup.Comment)) 

	# deleting all comments 
	[comment.extract() for comment in comments] 

	# delete script
	c=soup.findAll('script') 
	for i in c:
		i.extract()


	# get only the text from the <body> 
	body = soup.body(text=True) 

	trim = trimLines()
	body = [b.encode('euc-kr', 'ignore') for b in body if trim.filter(b)]
	text = ''.join(body) 
	return text
	


import sys
import codecs

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: url outfile"
		sys.exit(0)

	html = fetchurl_1(sys.argv[1])
	soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="euc-kr", convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
	txt = getOnlyText(soup)

	try:
		outfile = sys.argv[2]
		#out = codecs.open(outfile, encoding='euc-kr', mode='w+')
		out = open(outfile, mode='w+')
		out.write(txt)
		out.close()
	except:
		print "write fail:", outfile
		raise
		sys.exit(0)



