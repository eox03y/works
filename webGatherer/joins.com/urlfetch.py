#!/usr/bin/env python
import urllib
import urlparse
import httplib
import urllib2

#httplib.HTTPConnection.debuglevel = 1 

urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')

def get1(urlstr):
	print "\n========== get1()"
	fp = urllib.urlopen(urlstr)
	html = fp.read()
	print fp.headers
	print len(html)

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
	print r2.getheaders()
	print r2.getheader('location')


urlstr = "http://blog.joins.com/media/go_Random_Blog.asp"

#get2(urlstr)

import sys

if __name__ == "__main__":
	if len(sys.argv) > 1:
		getHEAD(sys.argv[1])
		get1(sys.argv[1])
	#import time
	#time.sleep(0.1)
