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

def get1(urlstr):
	fp = urllib.urlopen(urlstr)
	html = fp.read()
	print fp.headers
	print len(html)
	return html

def get2(urlstr):
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


urlstr = "http://blog.joins.com/media/go_Random_Blog.asp"

#get2(urlstr)


def get_text(htmltree):
	text = ""
	for item in htmltree:

		#print item, item.__class__.__name__
		if item.__class__.__name__ == "Tag":
			text += get_text(item)
		else:
			text += item
	return text


def saveLink(soup, out):
	for link in soup('a'):
		#print link
		try:
			out.write(link['href'])
			out.write('\n')
		except:
			continue

		#print link.contents
		try:
			link_name = get_text(link.contents)
			link_name = link_name.strip()
			print link_name
			out.write(link_name)
			out.write('\n\n')
		except:
			pass
		print


import sys
import codecs

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: url outfile"
		sys.exit(0)

	html = get1(sys.argv[1])
	soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="euc-kr")
	print soup.originalEncoding
	txt = soup.prettify("euc-kr")
	print type(txt)
	#mytxt = txt.decode().encode('euc-kr', 'ignore')
	mytxt =txt

	if len(sys.argv) < 2:
		print mytxt
		sys.exit(0)

	outfile = sys.argv[2]

	try:
		#out = codecs.open(outfile, encoding='euc-kr', mode='w+')
		out = open(outfile, mode='w+')
		out.write(mytxt)
	except:
		print "write fail:", outfile
		raise



