# -*- coding: utf-8 -*-
import codecs
import sys
import re
import unittest

from wikxml2wiki import ProcWiktionary
import wiktionaryparse as wp


reWIK_HEAD = re.compile(r'^\s*(=+)([^=]+)=+\s*$')
reCATEGORY = re.compile(r'^\s*\[\[Category:')
		
toSkipTitles = [ 'User:', 'Help:', 'Talk:', 'Appendix:', 'User talk:',
	'Wiktionary:', 'Wiktionary talk:' ]

toSkipHeads = [
	'Etymology',
	'Synonyms', 'Antonyms', 'Hyponyms',
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
		HEAD_FUNC_MAP = {'Pronunciation': 'parsePronunciation'}
		for data in self.L:
			if data.name.startswith('Pronunciation'):
				wp.parsePronunciation(data.items)
			elif data.name.startswith('Translation'):
				wp.parseTranslation(data.items)


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
		
	wiki2j.prn(outf)


class XmlToDict(ProcWiktionary):
	''' override '''
	def tt_handler(self, title, text):
		wiki2json(title, text, self.outf, debug=False)



if __name__=="__main__":
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	infile = sys.argv[1]
	outfile = sys.argv[2]
	procwik = XmlToDict()
	procwik.process(infile, outfile)
