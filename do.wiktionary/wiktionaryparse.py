# -*- coding: utf-8 -*-
import re

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

##### Pronunciation
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
	nation = ''
	ipa = ''
	xsampa = ''
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

def parsePronunciation(lines):
	for line in lines:
		if line.find('* {{audio|') != -1:
			line = get_audio_filename(line)
		else:
			phonetic = get_phonetic_notation(line)


##### Translation
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

def parseTranslation(lines):
	for line in lines:
		line = parse_langname(line)
		if line.startswith('* Old'):
			continue
		# skip if not the right format
		if len(line) and line[-1] != ':' and line.find('{{')==-1:
			continue
		if line.startswith('{{') and not line.startswith('{{trans-top'):
			continue

## items for word
def parseWord(lines):
	for line in lines:
		if line[:2]=='[[' and line[2:4] != 'en': 
			continue

		if line.startswith('[[Image'):
			pass	
		
		# remove wiki tag '[[ ~~~ ]]'
		line = filter_wiki_line(line)
		# remove '<ref>~~~</ref>'
		line = re.sub(r"<ref[^<]+</ref>", "", line, re.M)
		line = re.sub(r"<ref[^/]+/>", "", line, re.M)
		line = line.strip()

#####
if __name__=="__main__":
	import unittest
	class MyTest(unittest.TestCase):
		def test_audiofile(self):
			self.assertEqual(get_audio_filename(AUDIO.splitlines()[0]), 'en-uk-angel.ogg')
		def test_phonetic(self):
			self.assertEqual(get_phonetic_notation(PHONETIC.splitlines()[0]), ('UK', 'ˈdɪkʃən(ə)ɹi', '"dIkS@n(@)ri'))
			self.assertEqual(get_phonetic_notation(PHONETIC.splitlines()[1]), ('NA', 'ˈdɪkʃənɛɹi', '"dIkS@nEri'))

	unittest.main()
