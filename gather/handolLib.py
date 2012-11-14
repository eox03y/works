#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter

###
class DictWithCnt(dict):
        # key, value
	def add(self, key, cnt=0):
		self[key] = 1 + self.get(key, cnt)

	def rank(self):
		# rank high those which has high counter value
		return sorted(self.iteritems(), key=itemgetter(1), reverse=True)

	def prn(self, mincnt=0):
		# rank high those which has high counter value
		ranked = sorted(self.iteritems(), key=itemgetter(1), reverse=True)
		for (key, cnt) in ranked:
			if cnt > mincnt:
				print "%4d\t%s" % (cnt, key)
	def html(self, mincnt=0):
		self.prn(mincnt)
	

class DictWithUniq(dict):
"Dict that provides the uniqueness of key."
	def add(self, key, val=None):
	"return True only when the key is new and inserted"
		if self.get(key)==None:
			self[key] = val
			return True
		else:
			return False
	def load(self, fname):
	"load keys from the given file"
		try:
			fd = open(fname)
		except:
			print "Read fail: ", fname
			return 0
		cnt = 0
		for line in fd:
			flds = line.split()
			if self.add(flds[0]):
				cnt += 1
		fd.close()
		return cnt
		

	def save(self, fname):
	"overwrite keys to the given file"
		try:
			fd = open(fname, "w")
		except:
			print "Write fail: ", fname
			return 0
		cnt = 0
		for key in self.iterkeys():
			fd.write(key)
			fd.write('\n')
		fd.close()


import urllib
import urlparse
import urllib2
import BeautifulSoup


urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')

def fetchurl_1(urlstr, debug=0):
	fp = urllib.urlopen(urlstr)
	html = fp.read()
	if debug: print fp.headers
	if debug: print len(html)
	return html

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
	out.write("\n======\n")
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
"Get content lengh of the given url"
	#print getsize("https://www.djangoproject.com/m/img/site/hdr_logo.gif")
	#print getsize("http://upload.ybmbooks.com/action/loadFile.asp?dType=pub&siteCode=WW_BOK&subDir=www\upfile\DataRoom\&pVal=CB5AA1BFA8F25E4DDEEC994AEAC770EE2637191B6A6ED7019A664BFB6DA7FA5739AEFF417DFF6199B21522D5C57BF25A8C15E56490A5BF7C437A9F96EE02678219C4B66DD958C1FA32CA023C9ABA6A42")
	# 10965

	file = urllib.urlopen(uri)
	#print file.headers
	size = file.headers.get("content-length")
	file.close()
	flds = size.split(',')
	return int(flds[0])





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

	#print urllist

	for u in urllist:
		full_url = urlparse.urljoin(sys.argv[1], u)
		print full_url
		html = fetchurl_1(full_url)
		soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="euc-kr")
		urllist2 = saveLink(soup, 'a', out, pref='http://upload.ybmbooks.com/action/loadFile.asp')
		for u2 in urllist2:
			full_url2 = urlparse.urljoin(full_url, u2)
			size = getsize(full_url2)	
			#size = getHEAD_length(full_url2)	
			print size, " --- ", u2

if __name__=="__main__":
	if len(sys.argv) < 3:
		print "usage: filename field_list(comma-separated) delimiter(default=space)"
		sys.exit()

