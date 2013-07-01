# -*- coding: utf-8 -*-
import sys
import re
import codecs
import urllib
import json
import pprint

import anyReader
import wiktionparse as wp

'''
wiktionary page --> json
'''

#### Get XML via URL. 
## http://en.wiktionary.org/wiki/Special:Export/lion
def get_wiktion_xml(word):
	try:
		return get_wiktion_xml_gae(word)
	except:
		return get_wiktion_xml_local(word)

def get_wiktion_xml_gae(word):
	''' word --> wiktionary xml string '''
	from google.appengine.api import urlfetch

	url = 'http://en.wiktionary.org/wiki/Special:Export/%s' % (word)
	# Changing User-Agent
	# https://developers.google.com/appengine/docs/python/urlfetch/#Request_Headers
	# http://stackoverflow.com/questions/2743521/how-to-change-user-agent-on-google-app-engine-urlfetch-service
	result = urlfetch.fetch(url=url, 
				headers={"User-agent", "Jeenee/0.1 (handol; 2001-07-14)"}
			)
	if result.status_code == 200:
		return result.content.decode('utf-8')
	else:
		return ''

def get_wiktion_xml_local(word):
	''' word --> wiktionary xml string '''
	import urllib2

	url = 'http://en.wiktionary.org/wiki/Special:Export/%s' % (word)
	req = urllib2.Request(url)
	req.add_header("User-agent", "Jeenee/0.1 (handol; 2001-07-14)")
	fp = urllib2.urlopen(req)
	return fp.read().decode('utf-8')

#### Get title(WORD) and text(WIKI) from XML
## using re.compile() and re.search() 
'''
'''
reTITLE = re.compile(r'<title>\s*([^<]+)\s*</title>')
reTEXT = re.compile(r'<text [^>]*>\s*([^<]+)\s*</text>')
def get_xml2wikitext(wiktionxml):
	m1 = reTITLE.search(wiktionxml, re.M)
	if m1: title = m1.group(1)
	else: title = ''

	m2 = reTEXT.search(wiktionxml, re.M)
	if m2: text = m2.group(1)
	else: text = ''

	#return title.strip(),text.strip()
	return title, text


#### Get json object from wiki text
## using class WikiStructure()
'''
'''
def get_wiki2json(title, wikitext):
	wikistruct = WikiStructure(title)
	for line in wikitext.splitlines():
		wikistruct.feed(line)

	jsondata = wikistruct.get_json()
	return jsondata


#### main function: word --> json object
##
def get_word2json(word):
	title,wikitext = get_xml2wikitext( get_wiktion_xml(word) )

	wikistruct = WikiStructure(title)
	for line in wikitext.splitlines():
		wikistruct.feed(line)

	jsondata = wikistruct.get_json()
	return jsondata
	#return json.dumps(jsondata)			
	

####
#### Parsing Wikitionary Wiki Structure
####
reWIK_HEAD = re.compile(r'^\s*(=+)([^=]+)=+\s*$')
reCATEGORY = re.compile(r'^\s*\[\[Category:')
		
toSkipTitles = [ 'User:', 'Help:', 'Talk:', 'Appendix:', 'User talk:',
	'Wiktionary:', 'Wiktionary talk:' ]

toSkipHeads = [
	#'Etymology',
	'Synonyms', 'Antonyms', 'Hyponyms',
	'Holonyms', 'Coordinate',
	'Derived ', 'Related ',
	'References', 'Alternative', 'Statistics', 'Descendant',
	'Shorthand', 'Usage notes', 'thesaurus', 'See also',
	'External links', 'Quotations', 'Declension', 'Wiktionary:', 'Anagrams' ]


''' '''
def isToSkipTitle(title):
	for pf in toSkipTitles:
		if title.startswith(pf):
			return True
	return False

''' is it a English word ?'''
def isNotEnglish(title):
	for ch  in title:
		if ord(ch) > 255:
			return True
	ch = title[0]
	if not ch.isalnum() and ch != '-':
		return True
	return False

def isToSkipHead(headname):
	for h in toSkipHeads:
		if headname.startswith(h): 
			return True
	return False

## Store Wiki Header
class WikiHeading(object):
	def __init__(self, name, level, parent):
		self.name = name
		self.level = level
		self.items = []
		self.parent = parent
		self.children = []  # list of WikiHeading
	def addItem(self, item):
		self.items.append(item)

	def addChild(self, child):
		self.children.append(child)
		child.parent = self

	# recursive print-out
	def prn(self, out):
		if self.level==0:
			out.write("\n@ %s\n" % (self.name))
		else:
			indent = '=' * (self.level)
			out.write("%s %s\n" % (indent, self.name))

		indent = '  ' * (self.level)
		for i in self.items:
			out.write("%s%s\n" % (indent, i))
			pass
		for c in self.children:
			c.prn(out)

	# recursive conversion to json
	# return a dict {name: list}
	def conv_to_json(self):
		L = []

		if len(self.items) > 0:
			res_items = wp.conv_head_items(self.name, self.items)
			if len(res_items) > 0:
				if type(res_items)==list:
					L.extend( res_items )
				else:
					L.append( res_items )

		childD = {}
		for c in self.children:
			res_child = c.conv_to_json()
			if len(res_child) > 0:
				L.append ( res_child )
				#childD[c.name] = res_child

		if len(childD) > 0:
			L.append ( childD )
		return { self.name: L }
		
##
class WikiStructure:
	def __init__(self, word):
		self.ladder = [] # ladder of ancestors
		self.parent = None
		self.currhead = None
		self.add_heading(word, 0)
		self.roothead = self.currhead

		self.skipNonEnglish = False
		self.skipHead = False
		self.skipheadname = None
		self.skipheadlevel = None
		self.finished = False

	def prn(self, out=sys.stdout):
		self.roothead.prn(out)
		#for data in self.L:
		#	data.prn(out)

	def add_heading(self, headname, headlevel):
		newhead = WikiHeading(headname, headlevel, self.parent)
		if self.currhead and self.currhead.level < headlevel:
			# if newhead is the first or if newhead is a lower level
			self.ladder.append(self.currhead)
			self.parent = self.ladder[-1]
			self.parent.addChild(newhead)

		elif self.currhead and self.currhead.level > headlevel:
			# pop the ladder
			while len(self.ladder) > 0 and self.ladder[-1].level >= headlevel:
				self.ladder.pop()

			if len(self.ladder) > 0:
				self.parent = self.ladder[-1]
				self.parent.addChild(newhead)
		else:
			if self.parent:
				self.parent.addChild(newhead)

		self.currhead = newhead

	def feed(self, line):
		if self.finished:
			return
		line = line.strip()
		if len(line) == 0: 
			return
		if line.startswith('----'):
			self.finished = True
			return

		m = reWIK_HEAD.search(line)
		if m: 
			self.proc_head(m)
		else:
			if not self.skipNonEnglish:
				self.proc_item(line)

	def proc_head(self, m): 
		headlevel = len(m.group(1))
		headname = m.group(2)
		if headlevel == 2:
			if headname == 'English':
				# only English is processed
				self.skipNonEnglish = False
			else:
				self.skipNonEnglish = True
			return

		if self.skipNonEnglish:
			return

		if headlevel > 2:
			if not isToSkipHead(headname):
				# new data
				self.add_heading(headname, headlevel)
				if headlevel <= self.skipheadlevel:
					# skip ends
					self.skipHead = False
			else: 
				if not self.skipHead:
					# new skip 
					self.skipHead = True
					self.skipheadname = headname
					self.skipheadlevel = headlevel

	def proc_item(self, line):
		if reCATEGORY.search(line):
			return False
		self.currhead.addItem(line)

	def get_json(self):
		D = self.roothead.conv_to_json()
		return D

####
if __name__=="__main__":
	word = sys.argv[1]
	get_word2json(word)
	jsondata = get_word2json(word)
	pprint.pprint(jsondata)
	jsonstr = json.dumps(jsondata)

	'''
	outf = anyReader.anyWriter(sys.argv[2])

	title,wikitext = get_xml2wikitext( get_wiktion_xml(word) )

	wikistruct = WikiStructure(title)
	for line in wikitext.splitlines():
		wikistruct.feed(line)

	wikistruct.prn(outf)

	jsondata = wikistruct.get_json()
	jsonstr = json.dumps(jsondata)
	pprint.pprint(jsondata, stream=outf)
	#outf.write(jsonstr)
	'''	
