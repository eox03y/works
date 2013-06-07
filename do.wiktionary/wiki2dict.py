# -*- coding: utf-8 -*-
import codecs
import sys
import re
import unittest

from wikxml2wiki import ProcWiktionary


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
	'Statistics',
	'Descendant',
	'Shorthand',
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

AUDIO = '''* {{audio|en-uk-angel.ogg|Audio (UK)}}
* {{audio|en-us-angel.ogg|Audio (US)}}
'''
def get_audio_filename(line):
	flds = line.split('|')
	if len(flds)  > 2:
		return flds[1]
	else:
		return ''


PHONETIC = '''* {{a|UK}} {{IPA|/ˈdɪkʃən(ə)ɹi/}}, {{X-SAMPA|/"dIkS@n(@)ri/}}
* {{a|North America}} {{enPR|dĭk'shə-nĕr-ē}}, {{IPA|/ˈdɪkʃənɛɹi/}}, {{X-SAMPA|/"dIkS@nEri/}}
'''
curly_re = re.compile(r'\{\{([^\}]+)\}\}')
def get_phonetic_notation(line):
	trList = []
	parts = curly_re.findall(line)
	nation = None
	ipa = None
	xsampa = None
	for part in parts:
		flds = part.split('|')
		if flds[0]=='a':
			nation =  flds[1]
		elif flds[0]=='IPA':
			if flds[1][0]=='/' and flds[1][-1]=='/':
				ipa = flds[1][1:-1]
		elif flds[0]=='X-SAMPA':
			if flds[1][0]=='/' and flds[1][-1]=='/':
				xsampa = flds[1][1:-1]
	if nation.find(' ') != -1:
		flds = nation.split()
		nation = ''.join([f[0] for f in flds])
	return nation, ipa, xsampa

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
srch_langname = re.compile(r'^\*:? (\w+): \{\{t[^\|]?\|(\w+)\|')
# * Chinese:
# *: Mandarin: {{~~~ 
srch_langname_multi = re.compile(r'^\* (\w+):$')
langname_twocharcode_map = {} # 'ar':'Arabic', 'cmn':'Mandarin'
def parse_langname(line):
	# check multi-language (ex, Chinese)
	m = srch_langname_multi.search(line)
	if m:
		lang = m.group(1)
		if lang: return "* %s:" % (lang[:4])
		else: return line

	# normal case
	m = srch_langname.search(line)
	if m and m.group(1) and m.group(2):
		lang = m.group(1)
		abbr = m.group(2)
		short = lang[:4]
		line = line.replace(lang+':', short+':')
		#print "TRAN", lang, abbr
		#print line
		if not langname_twocharcode_map.has_key(abbr):
			langname_twocharcode_map[abbr] = [lang]
		elif not lang in langname_twocharcode_map[abbr]:
			langname_twocharcode_map[abbr].append(lang)
	return line

def prn_langname_code():
	for k,v in langname_twocharcode_map.iteritems():
		if type(v)==list:
			print '%3s --> %s' % (k, ','.join(v))
		else:
			print '%3s --> %s' % (k, v) 

'''
'''
def is_notgood(title):
	for ch  in title:
		if ord(ch) > 255:
			return True
	ch = title[0]
	if not ch.isalnum() and ch != '-':
		return True
	return False

'''
'''
from StringIO import StringIO
def wiki2dict(titleContent, textContent, outf, debug=False):
	outTitle = StringIO() 
	outBody = StringIO()
	if is_notgood(titleContent):
		return None

	for pf in skip_title_prefixes:
		if titleContent.startswith(pf):
			if debug: print "##SKIP TITLE", titleContent
			return None
	#outf.write("@ %s\n" % titleContent.strip())
	outTitle.write("@ %s\n" % titleContent.strip())

	isEnglishWord = False
	isSkip = False
	headname = ''
	headlevel = 0
	whySkip = None
	
	# remove html comment
	textContent = filter_wiki_multi(textContent)

	for line in textContent.splitlines():
		m = srch_wik_head1.search(line)
		# head line
		if m:
			#print "##RE", m.group(1), m.group(2)
			headlevel = len(m.group(1))
			headname = m.group(2)
			if headlevel == 2:
				if headname == 'English':
					isEnglishWord = True
				else:
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
			if not isSkip and headlevel > 2:
				#outf.write( "%s%s\n" % ('='*(headlevel-1), headname) )
				#outBody.write( "%s%s\n" % ('='*(headlevel-1), headname) )
				# if headlevel==2, then only 'English' is printed. so no need to print 'English'
				outBody.write( "=%d %s\n" % (headlevel, headname[:4]) )
				#print "%s%s" % ('='*(headlevel-1), headname[:3])
	
		# content lines in wiki
		else:
			skip_thisline = False
			line = line.strip()
			if srch_wik_category.search(line):
				isSkip =  True 

			if headname=='Pronunciation':
				if line.find('* {{audio|') != -1:
					line = get_audio_filename(line)
				else:
					phonetic = get_phonetic_notation(line)

			if headname.startswith('Translation'):
				line = parse_langname(line)
				if line.startswith('* Old'):
					skip_thisline = True
				# skip if not the right format
				'''
				* Ossetian:
					*: Digor: {{tø|os|авдисæр|tr=avdisær|sc=Cyrl}}
					*: Iron: {{tø|os|къуырисæр|tr=k”uyrisær|sc=Cyrl}}
				* Sami:
				*: Inari: vuossargâ
				*: Lule: mánnodahka
				'''
				if len(line) and line[-1] != ':' and line.find('{{')==-1:
					skip_thisline = True
					pass
				elif line.startswith('{{') and not line.startswith('{{trans-top'):
					skip_thisline = True

			if line[:2]=='[[' and line[2:4] != 'en': 
				skip_thisline = True

			if line.startswith('[[Image'):
				#outf.write(line+'\n')
				outBody.write(line+'\n')
			
			if not isSkip and not skip_thisline:
				# remove wiki tag '[[ ~~~ ]]'
				line = filter_wiki_line(line)
				# remove '<ref>~~~</ref>'
				line = re.sub(r"<ref[^<]+</ref>", "", line, re.M)
				line = re.sub(r"<ref[^/]+/>", "", line, re.M)
				line = line.strip()
				if len(line) > 0:
					#outf.write(line+'\n')
					outBody.write(line+'\n')

	# after for loop
	if isEnglishWord:
		outf.write(outTitle.getvalue())
		outf.write(outBody.getvalue())


class XmlToDict(ProcWiktionary):
	''' override '''
	def tt_handler(self, title, text):
		wiki2dict(title, text, self.outf, debug=False)



if __name__=="__main__":
	class MyTest(unittest.TestCase):
		def test_audiofile(self):
			self.assertEqual(get_audio_filename(AUDIO.splitlines()[0]), 'en-uk-angel.ogg')
		def test_phonetic(self):
			self.assertEqual(get_phonetic_notation(PHONETIC.splitlines()[0]), ('UK', 'ˈdɪkʃən(ə)ɹi', '"dIkS@n(@)ri'))
			self.assertEqual(get_phonetic_notation(PHONETIC.splitlines()[1]), ('NA', 'ˈdɪkʃənɛɹi', '"dIkS@nEri'))

	unittest.main()
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	infile = sys.argv[1]
	outfile = sys.argv[2]
	procwik = XmlToDict()
	procwik.process(infile, outfile)
