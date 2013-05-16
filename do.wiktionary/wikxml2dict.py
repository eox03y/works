#-- coding: utf-8 --
import codecs
import sys

import anyReader

import xml.sax
import xml.sax.handler

import re

srch_wik_head1 = re.compile(r'^\s*(=+)([^=]+)=+\s*$')
srch_wik_category = re.compile(r'^\s*\[\[Category:')
		
skip_title_prefixes = [
	'User:',
	'Help:',
	'Talk:',
	'Appendix:',
	'User talk:',
	'Wiktionary:',
	'Wiktionary talk:'
]

skip_head_names = [
	#'Translation',
	'Etymology',
	'Synonyms',
	'Antonyms',
	'Hyponyms',
	'Derived ',
	'Related ',
	'References',
	'Alternative',
	'Usage notes',
	'thesaurus',
	'See also',
	'External links',
	'Quotations',
	'Declension',
	'Wiktionary:',
	'Anagrams'
]

dont_skip_brkt_names = [
	'obsolete',

]

def check_if_skip_head(headname):
	for h in skip_head_names:
		if headname.startswith(h): 
			return True
	return False

def filter_wiki_multi(lines):
	return re.sub(r"<!--[^>]*-->", "", lines, re.M)

def filter_wiki_line(text):
	text = re.sub("<b>", " ", text)
	# Get rid of the word, we don't want it in the definition
	#text = re.sub(r"'''.*'''[ ]*(.*)", r"\1", text)
	text = re.sub("'''", "", text)
	text = re.sub("''", "", text)
	# Replace standard Wiki tags
	text = re.sub(r"\[\[[^\|]+\|([^\]]+)\]\]", r"\1", text)
	text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
	#text = re.sub(r"{{\(\|(.*)}}", r"", text)


	# Remove all unrecognized wiki tags
	#text = re.sub(r"{{[^}]+}}", "", text)
	return text


def get_audio_filename(line):
	flds = line.split('|')
	if len(flds)  > 2:
		return flds[1]
	else:
		return ''

## Translation
'''
===Translations
{{trans-top|shortened or contracted form of a word or phrase}}
* Arabic: {{t-|ar|اختصار|m|tr=ikhtiSaar}}
* Armenian: {{t-|hy|հապավում|tr=hapavum|sc=Armn}}
* Asturian: {{t+|ast|abreviatura|f}}
* Azeri: {{t-|az|abbreviatura}}
* Bulgarian: {{t+|bg|абревиатура|f|tr=abreviatúra}}
* Catalan: {{t+|ca|abreviatura|f}}
* Chinese:
*: Mandarin: {{t-|cmn|縮寫|sc=Hani}}, {{t-|cmn|缩写|tr=suōxiě|sc=Hani}}; {{t|cmn|簡寫|sc=Hani}}, {{t|cmn|简写|tr=jiǎnxiě|sc=Hani}}; {{t-|cmn|略語|sc=Hani}}, {{t|cmn|略语|tr=lüèyǔ|sc=Hani}}
* Cornish: {{t-|kw|berrheans}}

'''
# "* Arabic: {{t-|ar|اختصار|m|tr=ikhtiSaar}}" --> 'Arabic', 'ar'
srch_langname = re.compile(r'^\*:? (\w+): \{\{t[\-\+]?\|(\w+)\|')
langname_twocharcode_map = {} # 'ar':'Arabic', 'cmn':'Mandarin'
def parse_langname(line):
	m = srch_langname.search(line)
	if m and m.group(1) and m.group(2):
		#print "TRAN", m.group(1), m.group(2)
		if not langname_twocharcode_map.has_key(m.group(2)):
			langname_twocharcode_map[m.group(2)] = [m.group(1)]
		elif not m.group(1) in langname_twocharcode_map[m.group(2)]:
			langname_twocharcode_map[m.group(2)].append(m.group(1))

def prn_langname_code():
	for k,v in langname_twocharcode_map.iteritems():
		if type(v)==list:
			print '%3s --> %s' % (k, ','.join(v))
		else:
			print '%3s --> %s' % (k, v) 
'''
'''
def wiki2dict(titleContent, textContent, debug=False):
	'''
	parse text of 'text element' in 'wiktionary xml file'.
	'''
	for pf in skip_title_prefixes:
		if titleContent.startswith(pf):
			if debug: print "##SKIP TITLE", titleContent
			return None
	print "=", titleContent
	isSkip = False
	headname = ''
	headlevel = 0
	whySkip = None
	
	# remove html comment
	textContent = filter_wiki_multi(textContent)

	for line in textContent.splitlines():
		skip_thisline = False
		m = srch_wik_head1.search(line)
		# head line
		if m:
			#print "##RE", m.group(1), m.group(2)
			headlevel = len(m.group(1))
			headname = m.group(2)
			if headlevel == 2 and headname != 'English':
				if debug: print "##SKIP NonEnglish", headname
				isSkip =  True
				whySkip = (headlevel, headname)

			elif headlevel >= 2 and check_if_skip_head(headname):
				if debug: print "##SKIP HEAD", headname
				isSkip =  True
				whySkip = (headlevel, headname)
			elif whySkip==None or headlevel <= whySkip[0]:
				if debug: print "##TURNON HEAD", headname
				isSkip =  False
			else :
				pass
			if not isSkip:
				print "%s%s" % ('='*(headlevel-1), headname)
				#print "%s%s" % ('='*(headlevel-1), headname[:3])
	
		# content lines in wiki
		else:
			if srch_wik_category.search(line):
				isSkip =  True 

			if headname=='Pronunciation':
				if line.find('* {{audio|') == -1:
					'''
					skip sound notations
					* {{a|UK}} {{IPA|/ˈdɪkʃən(ə)ɹi/}}, {{X-SAMPA|/"dIkS@n(@)ri/}}
					* {{a|North America}} {{enPR|dĭk'shə-nĕr-ē}}, {{IPA|/ˈdɪkʃənɛɹi/}}, {{X-SAMPA|/"dIkS@nEri/}}
					'''
					skip_thisline = True
				else:
					line = get_audio_filename(line)

			if headname.startswith('Translation'):
				parse_langname(line)
				pass

			if line.startswith('[[Image'):
				print line
			elif line[:2]=='[[' and line[2:4] != 'en': 
				skip_thisline = True
			
			if not isSkip and not skip_thisline:
				# remove wiki tag '[[ ~~~ ]]'
				line = filter_wiki_line(line)
				# remove '<ref>~~~</ref>'
				line = re.sub(r"<ref[^<]+</ref>", "", line, re.M)				 
				line = re.sub(r"<ref[^/]+/>", "", line, re.M)				 
				line = line.strip()
				if len(line) > 0:
					print line

class WikXmlErrorHandler(xml.sax.handler.ErrorHandler):
	def error(self, exception):
		print exception.getMessage()
		print exception

	def fatalError(self, exception):
		print exception.getMessage()
		print exception

	def warning(self, exception):
		print exception.getMessage()


'''
input: xml file
do: parse xml file
output file: simplified wiki format

xml file: <page> <title> ~~~ </title>
				 <text> ~~~~~~~~~~~~~~~~~ </text> 
		</page>
'''
class WikXmlHandler(xml.sax.handler.ContentHandler):
	def __init__ (self):
		self.isPageElement = False
		self.isTitleElement = False
		self.titleContent = u""
		self.isTextElement = False
		self.textContent = u""

	def startElement(self, name, attrs):
		if name == 'page':
			self.isPageElement = True
		elif name == 'title':
			self.isTitleElement = True
			self.titleContent = ""
		elif name == 'text':
			self.isTextElement = True
			self.textContent = ""

	def endElement(self, name):
		if name == 'page':
			self.isPageElement= False
			#print "###TITLE"
			#print self.titleContent 
			#print "###TEXT"
			#print self.textContent
			wiki2dict(self.titleContent, self.textContent)
			self.titleContent = ""
			self.textContent = ""
		elif name == 'title':
			self.isTitleElement= False
		elif name == 'text':
			self.isTextElement = False

	def characters (self, ch):
		if self.isTitleElement:
			self.titleContent += ch
		elif self.isTextElement:
			self.textContent += ch


def proc_xmlfile(xmlfile):
	## Ways to construct a XMLReader object
	# simple way: 
	xmlreader = xml.sax.make_parser()
	# good way:
	# but, failed:  we have to implement parse()
	# refer: http://docs.python.org/2/library/xml.sax.reader.html#module-xml.sax.xmlreader
	#xmlreader = xml.sax.xmlreader.XMLReader()
	# better way: IncrementalParser.feed(data), close(, reset()
	#xmlreader = xml.sax.xmlreader.IncrementalParser()

	# Set UTF-8 stdout in case of the user piping our output
	reload(sys)
	sys.setdefaultencoding('utf-8')
	import codecs

	xmlreader.setContentHandler(WikXmlHandler())
	xmlreader.setErrorHandler(WikXmlErrorHandler())
	# xmlreader process 'byte stream' and assume the byte stream is utf-8.
	# so, we don't have to use 'codecs'. actually, we must not decode utf-8
	#infd = anyReader.anyReader(xmlfile, encoding='utf-8')
	infd = anyReader.anyReader(xmlfile, encoding='ascii')
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	# use parse()
	#xmlreader.parse(infd)

	# use feed()
	CHUNK = 100*1024

	try:
		for chunk in iter(lambda: infd.read(CHUNK), ''):
			#print "UNCOMPRESSED",len(chunk)
			#print chunk.decode('utf-8')
			xmlreader.feed(chunk)
	except:
		pass



'''
'''
def proc_wikifile(wikifile):
	text = open(wikifile).read()
	wiki2dict('', text)

if __name__=="__main__":
	infile = sys.argv[1]
	if infile.find('.xml') != -1:
		proc_xmlfile(infile)
	else:
		proc_wikifile(infile)
	prn_langname_code()
