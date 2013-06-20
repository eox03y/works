# -*- coding: utf-8 -*-
import codecs
import sys
import re
import unittest
import pprint

from wikxml2wiki import ProcWiktionary
import wiktionaryparse as wp


reWIK_HEAD = re.compile(r'^\s*(=+)([^=]+)=+\s*$')
reCATEGORY = re.compile(r'^\s*\[\[Category:')
		
toSkipTitles = [ 'User:', 'Help:', 'Talk:', 'Appendix:', 'User talk:',
	'Wiktionary:', 'Wiktionary talk:' ]

toSkipHeads = [
	'Etymology',
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

##
class WikiData(object):
	def __init__(self, name, level, parent):
		self.name = name
		self.level = level
		self.items = []
		self.parent = parent
		self.children = []  # list of WikiData
	def addItem(self, item):
		self.items.append(item)
	def addChild(self, child):
		self.children.append(child)
	def prn(self, out):
		if self.level==0:
			out.write("\n@ %s\n" % (self.name))
		else:
			indent = '==' * (self.level-1)
			out.write("%s %s\n" % (indent, self.name))

		indent = '  ' * (self.level-1)
		for i in self.items:
			out.write("%s%s\n" % (indent, i))
			pass

		
##
class Wiki2Json:
	def __init__(self, word):
		self.L = [] # list of WikiData object
		self.currdata = None
		self.add_data(word, 0)
		self.skipNonEnglish = False
		self.skipHead = False
		self.skipheadname = None
		self.skipheadlevel = None
		self.headname = None
		self.headlevel = None

	def prn(self, out=sys.stdout):
		for data in self.L:
			data.prn(out)

	def add_data(self, headname, headlevel):
		newdata = WikiData(headname, headlevel, self.currdata)
		self.headname = headname
		self.headlevel = headlevel
		self.L.append(newdata)
		self.currdata = newdata

	def feed(self, line):
		line = line.strip()
		if len(line) == 0: 
			return
		if line.startswith('----'):
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
				self.add_data(headname, headlevel)
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
		self.currdata.addItem(line)

	def parse_items(self):
		D = {}
		HEAD_FUNC_MAP = {'Pronunciation': 'parsePronunciation'}
		for data in self.L[1:]:
			val = {}
			if data.name.startswith('Pronunciation'):
				val = wp.parsePronunciation(data.items)
			elif data.name.startswith('Translation'):
				val = wp.parseTranslation(data.items)
			if val:
				D[data.name] = val
		R = {}
		#items = [i for i in self.L[0].items]
		items = {}
		items['audio'] = []
		items['image'] = []
		items['exstc'] = []
		items['meaning'] = []
		items['hword'] = []
		
		for line in self.L[0].items:
			if line[0]=='@':
				hline = u'<h3 class="hword"> %s </h3>\n' % (line[2:])
				items['hword'].append(line[2:])

			elif line[:2]=='#:':
				hline = u'<div class="exstc"> %s </div>\n' % (line[2:])
				items['exstc'].append(line[2:])

			elif line[0]=='#':
				items['meaning'].append(line[2:])
				hline = u'<div class="meaning"> %s </div>\n' % (line[2:])

			elif line.startswith('{{audio'):
				items['audio'].append(wp.get_sound_url(line))

			elif line.startswith('[[Image') or line.startswith('[[File'):
				items['image'].append(wp.get_image_url(line))

		items['ETC'] = D
		R[self.L[0].name] = items
		return R

'''
'''
from StringIO import StringIO
def wiki2json(title, text, outf, debug=False):
	if isNotEnglish(title):
		return None
	if isToSkipTitle(title):
		return None

	# remove html comment
	text = wp.filter_wiki_multi(text)

	wiki2j = Wiki2Json(title)
	for line in text.splitlines():
		wiki2j.feed(line)
		
	#wiki2j.prn(outf)
	D = wiki2j.parse_items()
	#pprint.pprint(D, stream=outf)

class XmlToDict(ProcWiktionary):
	''' override '''
	def tt_handler(self, title, text):
		wiki2json(title, text, self.outf, debug=False)


def wikiurl2jsonstr(wikiurl):
	procwik = XmlToDict()
	procwik.process(infile, outfile)

if __name__=="__main__":
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	infile = sys.argv[1]
	outfile = sys.argv[2]
	procwik = XmlToDict()
	procwik.process(infile, outfile)
