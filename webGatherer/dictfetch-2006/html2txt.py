#!/usr/bin/env python
# -*- coding: EUC-KR -*-
import HTMLParserHan
import urlparse

UNPAIRED_TAGS = [ 'meta', 'img', 'br', 'hr', 'col', 'input', 'index', 
					'basefont', 'link', 'base', 'area', 'param', 'isindex'  ]

NEWLINE_TAGS = ["br", "p", "tr", "table"]

NODATA_TAGS = [ 'script', 'style' ]

def swap_last_two(list):
	a = list.pop()
	b = list.pop()
	list.append(a)
	list.append(b)

class html2txt(HTMLParserHan.HTMLParser):
	def __init__(self, baseurl, debug=0):					
		HTMLParserHan.HTMLParser.__init__(self)
		self.baseurl = baseurl
		self.depth = 0
		self.stack = []
		self.data = ''
		self.debug = debug
		self.good = []
		self.anchors = []
		self._anchor_flag = 0
			
	def close(self):
		if self.debug:
			print '### Closing parser: line %d, col %d' % self.getpos()
			if len(self.rawdata):
				print	self.rawdata[:150]
				self.goahead(0)

	def	__pop(self, tag):
		if len(self.stack)==0:
			print '!! tag pair mismatch [%s] : ' % tag, 'line %d, column %d' % self.getpos()
			return []

		if tag not in self.stack:
			print '!! tag pair unmatched tag [%s] : ' % tag, \
				'line %d, column %d' % self.getpos()
			return []

		poped = []
		while len(self.stack):
			poped.append( self.stack.pop() )
			if poped[-1]==tag:
				break

		self.depth = len(self.stack)
		return poped

	def filter_anchor_url(self,a_url):
		if a_url[0]=='#': return 0
		if a_url.find(':') >= 0:
			if a_url.startswith('mailto')\
				or a_url.startswith('java'):
				return 0
		return 1

	def get_href_url(self, attrs):
		for name,value in attrs:
			if name=='href':
				if self.filter_anchor_url(value):
					return value
		return ''
	
	def	do_anchors(self, attrs):
		if self.debug: print attrs
		tmpurl = self.get_href_url(attrs)
		if tmpurl != '':
			newurl = urlparse.urljoin(self.baseurl, tmpurl)
			if self.debug: print tmpurl,'-->',newurl
			if newurl not in self.anchors:
				self.anchors.append( [newurl, None] )
				self._anchor_flag = 1

	def handle_starttag(self, tag, attrs):
		if tag in NEWLINE_TAGS:
			if self.data[-2:] != "\n\n":
				self.data += '\n'

		if tag not in UNPAIRED_TAGS:
			ment = 'S '
			if self.debug: print ' '*self.depth +'%-3d'%self.depth + ment, tag
			self.depth += 1
			self.stack.append(tag)
			if tag == 'a':
				self.do_anchors(attrs)
		else:
			ment = 'NP'
			if self.debug: print ' '*self.depth +'%-3d'%self.depth + ment, tag

	def handle_startendtag(self, tag, attrs):
		if self.debug:
			print ' '*self.depth +'%-3d'%self.depth + 'S/E '+ tag	
		
	def handle_endtag(self, tag):		
		poped = self.__pop(tag)
		if self.debug:
			if len(poped) > 1:
				msg = '*'*len(poped) +' ' + ','.join(poped)
				msg += ' line %d, column %d' % self.getpos()
			elif len(poped): 
				msg = poped[0]
			else:
				msg=''
			if self.debug: print ' '*self.depth +'%-3d'%self.depth + 'E '+ msg

	def handle_data(self, data):
		date = data.replace('\r\n', '\n')	
		data = data.strip()
		if len(data)>0: print "## %d" % ord(data[-1]), data
		if data != '':
			if self.stack[-1] not in NODATA_TAGS:
				if self.stack[-1] == 'a':
					#self.data = self.data.replace('\n',' ')
					if self._anchor_flag:
						self.anchors[-1][1] = data
						self._anchor_flag = 0
					pass
				self.data += data+'\n'
				# insert (tag, depth, contents)
				self.good.append( (self.stack[-1], len(self.stack), data ) )
			if self.debug: print ' '*self.depth, data

	def report_unbalanced(self, tag):
		print '???', tag
		self.depth -= 1
		
	def __find_root(self, curdepth, curidx):
	# return index. return -1 if not found
		for i in xrange(curidx-1, -1, -1):
			if self.good[i][1] < curdepth:
				return i
		return -1


	def info(self):
		print self.data

	def list(self):
		for url,ref in self.anchors:
			print "%s -- [%s]" % (url, ref)


if __name__ == "__main__":
	import geturl
	import sys

	#baseurl = "http://www.python.org"
	baseurl = "http://www.naver.com"
	if len(sys.argv) > 1: baseurl = sys.argv[1]

	html = geturl.geturl(baseurl)

	h2t = html2txt(baseurl, debug=0)
	
	h2t.feed( html.data)
	print '-'*50
	h2t.info()
	#h2t.list()
