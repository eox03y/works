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


def saveLink(soup, tagname, out, pref=''):
	urllist=[]
	for link in soup(tagname):
		#print link
		urladdr = link['href']
		if len(pref) > 0 and not urladdr.startswith(pref):
			continue

		urllist.append(urladdr)
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
		except:
			pass
		out.write('\n')
	return urllist
##

def getsize(uri):
    file = urllib.urlopen(uri)
    print file.headers
    size = file.headers.get("content-length")
    file.close()
    flds = size.split(',')
    return int(flds[0])

#print getsize("https://www.djangoproject.com/m/img/site/hdr_logo.gif")
#print getsize("http://upload.ybmbooks.com/action/loadFile.asp?dType=pub&siteCode=WW_BOK&subDir=www\upfile\DataRoom\&pVal=CB5AA1BFA8F25E4DDEEC994AEAC770EE2637191B6A6ED7019A664BFB6DA7FA5739AEFF417DFF6199B21522D5C57BF25A8C15E56490A5BF7C437A9F96EE02678219C4B66DD958C1FA32CA023C9ABA6A42")
# 10965




###

import sys
import codecs

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: url outfile"
		sys.exit(0)

	html = fetchurl_1(sys.argv[1])
	soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="euc-kr")

	#for i in dir(soup):
	#	print i

	#print "HEAD:", soup.head


	try:
		outfile = sys.argv[2]
		#out = codecs.open(outfile, encoding='euc-kr', mode='w+')
		out = open(outfile, mode='w+')
		urllist = saveLink(soup, 'a', out, pref='/reader/reader_read.asp')
	except:
		print "write fail:", outfile
		raise
		sys.exit(0)

	print urllist

	for u in urllist:
		html = fetchurl_1(u)
		soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="euc-kr")
		saveLink(soup, 'a', out, pref='http://upload.ybmbooks.com/action/loadFile.asp')
