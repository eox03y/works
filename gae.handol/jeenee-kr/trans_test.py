# -*- coding: utf-8 -*-
import re
import json
import pprint
from StringIO import StringIO

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
		if pos == -1: return ''
		lang = line[:pos]
		line = line[pos+2:]
		if line.find('{{') != -1:
			trList = proc_tr_curly(line)
		elif line.find('[[') != -1:
			trList = proc_tr_square(line)
		else:
			return ' ',[]

		return lang, trList

	def prn(self):
		pprint.pprint(self.D)

	def html(self):
		out = StringIO()
		for meaning,langlist in self.D.iteritems():
			out.write('<div class="trmean"> %s \n' % (meaning))

				for lang,trlist in langlist:
					out.write('<div class="trlang"> %s \n' % (lang))
					for tr in trlist:
						out.write('<div class="trword"> %s </div> ' % (tr[0]))
						out.write('<div class="trsnd"> %s </div> \n' % (tr[1]))
					out.write('</div>')
			out.write('</div>')
		return out.getvalue()



AAA = '''
{{trans-top|to present again or anew}}
* Catalan: {{t+|ca|representar}}
* Dutch: {{t+|nl|voorstellen}}
* French: {{t+|fr|représenter}}
{{trans-mid}}
* Romanian: {{t-|ro|reprezenta}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-bottom}}

{{trans-top|to portray by pictorial or plastic art}}
* Catalan: {{t+|ca|representar}}
* Dutch: [[voorstellen]], [[uitbeelden]], ergens [[voor staan]]
* Finnish: {{t+|fi|kuvata}}
* French: {{t+|fr|représenter}}
{{trans-mid}}
* Romanian: {{t-|ro|reprezenta}}
* [[Scottish Gaelic]]: {{t-|gd|riochdaich}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-bottom}}

{{trans-top|to portray by mimicry or action of any kind}}
* Dutch: {{t+|nl|voorstellen}}
* Finnish: {{t+|fi|kuvata}}
* French: {{t+|fr|jouer}}
{{trans-mid}}
* [[Scottish Gaelic]]: {{t-|gd|riochdaich}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-bottom}}

{{trans-top|to stand in the place of}}
* Arabic: {{Arab|[[مثل]]}} {{IPAchar|(máθθala)}}
* Catalan: {{t+|ca|representar}}
* Chinese: [[代表]] (dàibiǎo)
* Czech: {{t-|cs|reprezentovat}}, {{t-|cs|zastupovat}}
* Dutch: {{t+|nl|vertegenwoordigen}}, {{t+|nl|representeren}}
* Finnish: {{t+|fi|edustaa}}
* French: {{t+|fr|représenter}}
* German: {{t+|de|darstellen}}, {{t+|de|repräsentieren}}
* Hungarian: {{t+|hu|képvisel}}
{{trans-mid}}
* Italian: {{t+|it|rappresentare}}
* Japanese: [[代表]]する (daihyō suru)
* Korean: [[대표하다]] (daepyohada)
* Portuguese: {{t+|pt|representar}}
* Romanian: {{t-|ro|reprezenta}}
* Russian: [[представлять]] (predstavlját’)
* [[Scottish Gaelic]]: {{t-|gd|riochdaich}}
* Spanish: {{t+|es|representar}}
* Swahili: {{t+|sw|wakilisha}}
* Swedish: {{t+|sv|representera}}
{{trans-bottom}}

{{trans-top|to exhibit to another mind in language}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-mid}}
{{trans-bottom}}

{{trans-top|to serve as a sign or symbol of}}
* Dutch: {{t+|nl|voorstellen}}
* Finnish: {{t+|fi|edustaa}}
* Portuguese: {{t+|pt|representar}}
{{trans-mid}}
* Romanian: {{t-|ro|reprezenta}}
* [[Scottish Gaelic]]: {{t-|gd|riochdaich}}
* Spanish: {{t|es|representar}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-bottom}}

{{trans-top|to bring a sensation of into the mind or sensorium}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-mid}}
{{trans-bottom}}

{{trans-top|to form or image again in consciousness, as an object of cognition or apprehension}}
* Romanian: {{t-|ro|reprezenta}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-mid}}
{{trans-bottom}}

{{checktrans-top}}
* {{ttbc|eo}}: [[reprezenti]]
* {{ttbc|it}}: [[rappresentare]]
{{trans-bottom}}

'''


### run the test
if __name__=='__main__':
	trinfo = TrInfo()

	for line in AAA.splitlines():
		trinfo.proc(line)
	trinfo.prn()
