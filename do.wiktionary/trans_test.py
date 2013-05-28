# -*- coding: utf-8 -*-
import re

srch_trans_pos = re.compile(r'([^\}]+)\}\}')

def get_translation_div(trnsline):
	line = trnsline[2:]
	pos = line.find(':')
	if pos == -1: return ''
	lang = line[:pos]
	parts = line.split('{{')
	cnt = 0
	for part in parts[1:]:
		m = srch_trans_pos.search(part)
		if m: 
			cnt += 1 
			print "%d %s" % (cnt, m.group(1))

	return  line

AAA = '''
* Dutc: {{t+|nl|afkeurenswaardig}}, {{t+|nl|schuldig}}
* Finn: {{t-|fi|moitittava}}, {{t-|fi|tuomittava}}
* Germ: {{t+|de|verwerflich}}
* Gree: {{t+|el|αξιόμεμπτος|m|tr=axiómemptos|sc=Grek}}, {{t+|el|κατακριτέος|m|tr=katakritéos|sc=Grek}}
* Icel: {{t-|is|ámælisverður}}
* Norw: {{t-|no|klanderverdig}}
* Russian: {{l|ru|достойный}} {{l|ru|осуждение|осуждения}} (dostójnyj osuždénija), {{t+|ru|предосудительный|tr=predosudítelʹnyj|sc=Cyrl}}
* Span: {{t-|es|reprehensible}}
{{trans-top|deserving of reprehension}}
* Dutc: {{t-|nl|verwerpelijk}}, {{t+|nl|afkeurenswaardig}}
* Gree: {{t+|el|αξιόμεμπτος|m|tr=axiómemptos|sc=Grek}}, {{t+|el|κατακριτέος|m|tr=katakritéos|sc=Grek}}'''

for line in AAA.splitlines():
	print line
	print get_translation_div(line)
