# -*- coding: utf-8 -*-
import re
import md5
import json
import pprint
from StringIO import StringIO

# my py files

def filter_wiki_multi(lines):
	return re.sub(r"<!--[^>]*-->", "", lines, re.M)

def filter_wiki_line(text):
	text = re.sub(r"<!--[^>]*-->", "", text, re.M)
	text = re.sub("<b>", " ", text)
	# Get rid of the word, we don't want it in the definition
	#text = re.sub(r"'''.*'''[ ]*(.*)", r"\1", text)
	text = re.sub("'''", "", text)
	text = re.sub("''", "", text)
	# Replace standard Wiki tags
	text = re.sub(r"\[\[[^\|]+\|([^\]]+)\]\]", r"\1", text)
	text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
	#text = re.sub(r"{{\(\|(.*)}}", r"", text)


	if text.find('{{') != -1:
		text = proc_curly(text)
	# Remove all unrecognized wiki tags
	#text = re.sub(r"{{[^}]+}}", "", text)
	return text

#
reCURLY = re.compile(r'\{\{([^\}]+)\}\}')
def	proc_curly(line):
	m = reCURLY.search(line)
	if m:
		curly = m.group(1)
		flds = curly.split('|')
		if len(flds) >= 2: found = flds[1]
		else: found = flds[0]
		res = re.sub(reCURLY, '<em>(%s)</em>' % (found), line, 1)
		return res	
	else:
		return line


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
	D = {}
	for line in lines:
		if line.find('* {{audio|') != -1:
			audio = get_audio_filename(line)
			audio_url = get_sound_url(audio)
			if D.has_key('audio'):
				D['audio'].append(audio_url)
			else:
				D['audio'] = [audio_url]
		else:
			nation, ipa, xsampa = get_phonetic_notation(line)
			D['sndsign']= {'nation': nation, "IPA": ipa, "XSAMPA": xsampa}
	return D


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




'''
input: t+|el|αξιόμεμπτος|m|tr=axiómemptos|sc=Grek
output: ('αξιόμεμπτος', 'axiómemptos')
output: ('αξιόμεμπτος', '')
'''
def parse_tr_body(trbody):
	flds = trbody.split('|')
	if len(flds) < 3: return None
	trword = flds[2] # translated word
	snd = '' # sound of the translated word is optional
	if len(flds) >= 5 and flds[4].startswith('tr='):
		snd = flds[4][3:] # sound of the translated word
	return (trword, snd)


'''
input: {{trans-top|deserving of reprehension}}
output: deserving of reprehension
'''
def proc_tr_meaning(mline):
	mline = mline[2:]
	if not mline.startswith('trans-'):
		return None
	flds = mline.split('|')
	if  len(flds) < 2: 
		return None
	meaning = flds[1][:-2]
	return meaning

'''

* Arabic: {{Arab|[[ﻢﺜﻟ]]}} {{IPAchar|(máθθala)}}
* Catalan: {{t+|ca|representar}}
'''
#curly_re = re.compile(r'([^\}]+)\}\}')
curly_re = re.compile(r'\{\{([^\}]+)\}\}')
def proc_tr_curly(line):
	trList = []
	parts = curly_re.findall(line)
	for part in parts:
		tr_word_n_snd = parse_tr_body(part)
		if tr_word_n_snd:
			trList.append(tr_word_n_snd)
	return trList

'''
* Chinese: [[代表]] (dàibiǎo)
* Japanese: [[代表]]する (daihyō suru)
'''
sq_re = re.compile(r'.*\[\[([^\]]+)\]\]([^\s]*)\s+\(([^\)]+)\)')
def proc_tr_square(line):
	m = sq_re.search(line)
	if not m: return []
	trword = m.group(1)+m.group(2)
	snd = m.group(3)
	return [(trword, snd)]

class TrInfo:
	def __init__(self):
		self.D = {}
		self.meaning = ''

	def proc(self, line):
		line = line.strip()
		if len(line)==0:
			return

		if line[0]=='*':
			lang, trList = self.proc_tr_line(line)
			if len(lang) and len(trList):
				langList = self.D.get(self.meaning, None)
				if not langList: 
					langList = {}
					self.D[self.meaning] = langList
				langList[lang] = trList

		elif line[0]=='{':
			meaning = proc_tr_meaning(line)
			if meaning:
				self.meaning = meaning
		
	def proc_tr_line(self, trnsline):
		line = trnsline[2:]
		pos = line.find(':')
		if pos == -1: return '',[]
		lang = line[:pos]
		line = line[pos+2:]
		if line.find('{{') != -1:
			trList = proc_tr_curly(line)
		elif line.find('[[') != -1:
			trList = proc_tr_square(line)
		else:
			return '',[]

		return lang, trList

	def prn(self):
		pprint.pprint(self.D)

	def html(self):
		out = StringIO()
		for meaning,langlist in self.D.iteritems():
			out.write('<ul class="trmean"> %s \n' % (meaning))
			for lang,trlist in langlist.iteritems():
				out.write('\t<li class="trlang"> %s ' % (lang))
				for tr in trlist:
					out.write('<div class="trword"> %s </div>' % (tr[0]))
					out.write('<div class="trsnd"> %s </div>' % (tr[1]))
				out.write('</li>\n')
			out.write('</ul>\n')
		return out.getvalue()


def parseTranslation(lines):
	trinfo = TrInfo()

	for line in lines:
		trinfo.proc(line)
	return trinfo.D

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

## SOUND AUDIO (OGG) FILE
def get_sound_url(oggfile):
	m = md5.new()
	oggfile = oggfile[0].upper() + oggfile[1:]
	m.update(oggfile)
	hexkey = m.hexdigest()
	folder = u'%s/%s' % (hexkey[0], hexkey[:2])
	sndurl = 'http://upload.wikimedia.org/wikipedia/commons/%s/%s' % (folder, oggfile)
	return sndurl

def get_sound_div(oggfile):
	sndurl = get_sound_url(oggfile)
	snddiv = u''' <div class="mediaContainer" style="position:relative;display:block;width:175px">
	<audio id="mwe_player_0" style="width:175px;height:23px" poster="//bits.wikimedia.org/static-1.22wmf4/skins/common/images/icons/fileicon-ogg.png" controls="" preload="none" class="kskin" data-durationhint="1.3815873015873" data-startoffset="0" data-mwtitle="%s" data-mwprovider="wikimediacommons">
	<source src="%s" type="audio/ogg; codecs=&quot;vorbis&quot;" data-title="Original Ogg file (107 kbps)" data-shorttitle="Ogg source" data-width="0" data-height="0" data-bandwidth="107280">
	</source></audio></div> ''' % (oggfile, sndurl)
	return snddiv

###  IMAGE file (Image:,  File:)
'''
[[Image:Lion waiting in Nambia.jpg|thumb|right|250px|A lion.]]
'''
def get_image_url(imgdesc):
	imgdesc = imgdesc[8:-2]
	flds = imgdesc.split('|')
	if len(flds) < 2:
		return ''

	pxsize = '800'
	for fld in flds:
		if fld.endswith('px'):
			pxsize = fld[:-2].strip()
			break

	imgfile = flds[0].replace(' ', '_')
	imgfile = imgfile[0].upper() + imgfile[1:]
	desc = flds[-1]	
	m = md5.new()
	m.update(imgfile)
	hexkey = m.hexdigest()
	folder = u'%s/%s' % (hexkey[0], hexkey[:2])
	#imgurl = u'http://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%spx-%s' % (folder, imgfile, pxsize, imgfile)
	imgurl = u'http://upload.wikimedia.org/wikipedia/commons/%s/%s' % (folder, imgfile)
	return imgurl, desc

##
def get_image_div(imgdesc):
	imgurl, desc = get_image_url(imgdesc)
	imgdiv = u'''<div class="dictimg"> <img class="img-polaroid" height="200px" width=auto src="%s"> %s </img></div>\n''' % (imgurl, desc)
	return imgdiv

#####
##
def conv_head_items(headname, items):
	val = None
	if headname.startswith('Pronunciation'):
		val = parsePronunciation(items)
	elif headname.startswith('Translation'):
		val = parseTranslation(items)
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
			hline = '<h3 class="hword"> %s </h3>\n' % (line[2:])
			items['hword'].append(line[2:])

		elif line[:2]=='#:':
			hline = '<div class="exstc"> %s </div>\n' % (line[2:])
			text = filter_wiki_line(line[2:])
			items['exstc'].append(text)

		elif line[0]=='#':
			hline = '<div class="meaning"> %s </div>\n' % (line[2:])
			text = filter_wiki_line(line[2:])
			items['meaning'].append(text)

		elif line.startswith('[[Image') or line.startswith('[[File'):
			items['image'].append(get_image_url(line))

	R = {}
	for k,v  in items.iteritems():
		if v != []:
			R[k] = v
	return R



#####
if __name__=="__main__":
	import unittest
	class MyTest(unittest.TestCase):
		def test_proc_curly(self):
			self.assertEqual(proc_curly('{{context|obsolete|lang=en}}'), '<em>(obsolete)</em>')
			self.assertEqual(proc_curly('{{context|obsolete|lang=en}} high ho'), '<em>(obsolete)</em> high ho')
			self.assertEqual(proc_curly('{{w|Robert Burton}}'), '<em>(Robert Burton)</em>')
			self.assertEqual(proc_curly('{{defdate|16th-18th c.}}'), '<em>(16th-18th c.)</em>')
		def test_audiofile(self):
			self.assertEqual(get_audio_filename(AUDIO.splitlines()[0]), 'en-uk-angel.ogg')
		def test_phonetic(self):
			self.assertEqual(get_phonetic_notation(PHONETIC.splitlines()[0]), ('UK', 'ˈdɪkʃən(ə)ɹi', '"dIkS@n(@)ri'))
			self.assertEqual(get_phonetic_notation(PHONETIC.splitlines()[1]), ('NA', 'ˈdɪkʃənɛɹi', '"dIkS@nEri'))

	unittest.main()
