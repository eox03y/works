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
		for c in self.children:
			c.prn(out)

	def conv_to_json(self, D):
		res = conv_head_items(self.name, self.items)
		D[self.name] = res
		for c in self.children:
			c.conv_to_json(D)
		

		
##
class Wiki2Json:
	def __init__(self, word):
		#self.L = [] # list of WikiHeading object
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
			self.currhead.addChild(newhead)
			self.ladder.append(self.currhead)
			self.parent = self.ladder[-1]

		elif self.currhead and self.currhead.level > headlevel:
			# pop the ladder
			while True:
				self.ladder.pop()
				if  len(self.ladder) == 0: break
				if self.ladder[-1].level <= headlevel: break

			if len(self.ladder) > 0:
				self.parent = self.ladder[-1]

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
		D = {}	
		self.roothead.conv_to_json(D)
		return D

##
def conv_head_items(headname, items):
	val = None
	if headname.startswith('Pronunciation'):
		val = wp.parsePronunciation(items)
	elif headname.startswith('Translation'):
		val = wp.parseTranslation(items)
	else:
		val = conv_items(items)

	return val

def conv_items(orgitems):
	items = {}
	items['audio'] = []
	items['image'] = []
	items['exstc'] = []
	items['meaning'] = []
	items['hword'] = []
	
	for line in orgitems:
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

	R = {}
	for k,v  in items.iteritems():
		if v != []:
			R[k] = v
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
		
	wiki2j.prn(outf)
	D = wiki2j.get_json()
	pprint.pprint(D, stream=outf)

class XmlToDict(ProcWiktionary):
	''' override '''
	def tt_handler(self, title, text):
		wiki2json(title, text, self.outf, debug=False)


def wikiurl2jsonstr(wikiurl):
	procwik = XmlToDict()
	procwik.process(infile, outfile)

if __name__=="__main__":
	#a = WikiHeading('root', 1, None)
	#print isinstance(a, WikiHeading)

	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	infile = sys.argv[1]
	outfile = sys.argv[2]
	procwik = XmlToDict()
	procwik.process(infile, outfile)
