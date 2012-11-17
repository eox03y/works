#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
import shutil

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
	

###
class DictWithUniq(dict):
	""" Dict that provides the uniqueness of key."""
	def add(self, key, val=None):
		"""return True only when the key is new and inserted"""
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


###
import urllib
import urlparse
import BeautifulSoup

urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')

###
def fetchUrl(urlstr, debug=0):
	""" return HTML string and charset """
	fp = urllib.urlopen(urlstr)
	html = fp.read()
	charset = fp.headers.getparam('charset')
	if charset==None: charset = 'euc-kr'
	if debug: print fp.headers
	if debug: print len(html)
	return html, charset


###
def sizeUrl(uri):
	""" return 'content-length' of a give URL """
	file = urllib.urlopen(uri)
	#print file.headers
	try:
		size = file.headers.get("content-length")
	except:
		return 0
	file.close()
	flds = size.split(',')
	return int(flds[0])

###
def getLinkName(htmltree):
	""" Using BeautifulSoup
	<a href="/user/add?"> go get it </a>  
	---> go get it
	"""

	text = ""
	for item in htmltree:

		#print item, item.__class__.__name__
		if item.__class__.__name__ == "Tag":
			text += getLinkName(item)
		else:
			text += item
	return text.strip()

###
import time
import logging

class webCrawl:
	def __init__(self):
		self.rootUrl = None
		self.visitUrlPrefix = None
		self.actionUrlPrefix = None
		self.toVisit = []
		self.visited = DictWithUniq()
		self.pauseSec = 0.1
		self.visitSave = None

	def load(self, fname):
		self.visitSave = fname
		cnt = self.visited.load(fname)
		print "%d loaded from %s" % (cnt, fname)
		logging.info("%d loaded from %s" % (cnt, fname))

	def start(self, url, hfile="harvest.dat", vprefix=None, aprefix=None, pause=0.1):
		logging.info("START vprefix[%s] aprefix[%s]" % (vprefix, aprefix))
		self.rootUrl = url
		self.visitUrlPrefix = vprefix
		self.actionUrlPrefix = aprefix
		self.harvestFile = hfile
		self.pauseSec = pause
		self._add_to_visit(self.rootUrl)
		self._do_crawl()

	
	def _add_to_visit(self, new_url):
		""" add a new url into "to visiti Queue" if prefix of the url match.
		    return 1 if added
		"""
		if self.visitUrlPrefix!=None and (not new_url.startswith(self.visitUrlPrefix)): 
			return 0
		# check if the url was visited before
		if new_url in self.visited: 
			return 0

		#else
		self.toVisit.append(new_url)
		return 1

	
	def _do_action(self, act_url, link_name):
		print act_url
		if self.actionUrlPrefix!=None and (not act_url.startswith(self.actionUrlPrefix)): 
			return 0
		logging.info("ACT %s [%s]" % (act_url, link_name))
		size = sizeUrl(act_url)	
		line = "%s [%d] [%s]\n" % (act_url, size, link_name)
		#print line
		fd = open(self.harvestFile, "a")
		fd.write(line)
		fd.close()
		
		self.visited.add(act_url)
		return 1
		
	def _do_visit(self, curr_url):
		""" read a url and extract links from HTML """
		time.sleep(self.pauseSec)
		html, charset = fetchUrl(curr_url)
		soup = BeautifulSoup.BeautifulSoup(html, fromEncoding=charset)

		logging.info("VISIT %s [%d]bytes char-set=%s" % (curr_url, len(html), charset))
		cnt_children = 0
		for link in soup('a'):
			try:
				child_addr = link['href']
			except:
				continue
			full_url = urlparse.urljoin(curr_url, child_addr)

			cnt_children += self._add_to_visit(full_url)
			
			link_name = getLinkName(link.contents)
			self._do_action(full_url, link_name)
		logging.info("CHILDREN %d added for visit" % cnt_children)
	
	def _do_crawl(self):
		while len(self.toVisit) > 0:
			current = self.toVisit.pop(0)
			# check if the url was visited before
			if current in self.visited: continue	
			self._do_visit(current)
			# mark as 'visited' after finishing visit
			self.visited.add(current)

		#
		try:
			shutil.copyfile(self.visitSave, self.visitSave + ".org")
		except:
			pass
		self.visited.save(self.visitSave)


###

import sys
import codecs

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: url outfile"
		sys.exit(0)

	logging.basicConfig(filename="webcrwal.log", level=logging.INFO,
		format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

	crawler = webCrawl()
	crawler.load("visited.dat")
	crawler.start(sys.argv[1],
		 vprefix='http://www.ybmbooks.com/reader/reader',
		 aprefix='http://upload.ybmbooks.com/action/loadFile')

	

