#!/usr/bin/env python
# -*- coding: euc-kr -*-
import urllib

#httplib.HTTPConnection.debuglevel = 1 

urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')

def getcharsethtml(html):
	import re
	pattern = re.compile("charset=([a-z0-9-]+)", re.I)
	s = pattern.search(html)
	if s==None:
		return None
	else:
		charset = s.group().split('=')[1]
	return charset
	

def geturl(urlstr, default="euc-kr"):
	"""
	return charset and html text
	"""
	if not urlstr.startswith("http://"):
		urlstr = "http://%s" % urlstr

	fp = urllib.urlopen(urlstr)

	# get charset value
	charsets = [] 
	for p in fp.headers.plist:
		p = p.lower()
		flds = p.split('=')
		if len(flds)==2 and flds[0]=="charset":
			charsets.append(flds[1])
			break

	html = fp.read()

	charset = getcharsethtml(html)
	if len(charsets)==0 or charset != charsets[0]:
		charsets.append(charset)

	return fp.headers.type, charsets, html


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

def savefile(text, fname, fromcharset, tocharset):
	try:
		print "writing file: %s" % ( fname)
		out = codecs.open(fname, encoding=tocharset, mode='w+')
		out.write(unicode(text, encoding=fromcharset))
	except:
		print "write fail:", fname
		raise


def SaveUrl(urlstr, fname, tocharset, debug=1):
	contenttype, charsets, html = geturl(urlstr)
	if debug:
		print "TYPE: %s  CHARSET: %s LENG: %d" % (contenttype, charsets, len(html))

	for charset in charsets:
		try:
			savefile(html, fname, charset, tocharset)
			print """saved "%s" in "%s", org charset=%s """ % (fname, tocharset, charset)
			break
		except:
			print """charset "%s" seems to be NOT correct""" % (charset)
			raise
			pass
		
	
urlstr = "http://blog.joins.com/media/go_Random_Blog.asp"


if __name__ == "__main__":
	import sys
	import codecs

	if len(sys.argv) < 3:
		print "usage: url outfile [output-charset]"
		sys.exit(0)


	if len(sys.argv) == 4:
		tocharset = sys.argv[3]
	else:
		tocharset = "utf-8"
	
	SaveUrl(sys.argv[1], sys.argv[2], tocharset)



