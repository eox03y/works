# -*- coding: utf-8 -*-
import sys
import re
import codecs
import urllib
import pprint
import anyReader

'''
wiktionary page --> json
'''


## Changing User-Agent
# req.add_header("User-agent", "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4")
# https://developers.google.com/appengine/docs/python/urlfetch/#Request_Headers
# http://stackoverflow.com/questions/2743521/how-to-change-user-agent-on-google-app-engine-urlfetch-service
def get_wiktion_xml(word):
	try:
		return get_wiktion_xml_gae(word)
	except:
		return get_wiktion_xml_local(word)

def get_wiktion_xml_gae(word):
	''' word --> wiktionary xml string '''
	from google.appengine.api import urlfetch

	url = 'http://en.wiktionary.org/wiki/Special:Export/%s' % (word)
	result = urlfetch.fetch(url=url, 
				headers={"User-agent", "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4"}
			)
	if result.status_code == 200:
		return result.content
	else:
		return None

def get_wiktion_xml_local(word):
	''' word --> wiktionary xml string '''
	import urllib2

	url = 'http://en.wiktionary.org/wiki/Special:Export/%s' % (word)
	req = urllib2.Request(url)
	req.add_header("User-agent", "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4")
	fp = urllib2.urlopen(req)
	return fp.read()


'''
'''
reTITLE = re.compile(r'<title>\s*([^<]+)\s*</title>')
reTEXT = re.compile(r'<text [^>]*>\s*([^<]+)\s*</text>')
def get_wikitext(wiktionxml):
	print type(wiktionxml)
	m1 = reTITLE.search(wiktionxml, re.M)
	if m1: title = m1.group(1)
	else: title = None

	m2 = reTEXT.search(wiktionxml, re.M)
	if m2: text = m2.group(1)
	else: text = None

	return title.strip(),text.strip()


'''
'''
def get_wiki2json(title, wikitext):
	import wiki2json
	wiki2j = wiki2json.Wiki2Json(title)
	for line in text.splitlines():
		wiki2j.feed(line)

	#wiki2j.prn(outf)
	D = wiki2j.parse_items()
	#pprint.pprint(D, stream=outf)
	return D


if __name__=='__main__':
	ti,text = get_wikitext( get_wiktion_xml(sys.argv[1]) )
	print ti, len(text), 'chars'
	D = get_wiki2json(ti, text)
	outf = anyReader.anyWriter(sys.argv[2])
	pprint.pprint(D, stream=outf)
		