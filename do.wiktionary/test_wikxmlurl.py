from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import QName
import urllib
urllib.URLopener.version = (
	'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '
	'Gecko/20050609 Firefox/1.0.4')

url = 'http://en.wiktionary.org/wiki/Special:Export/lion'
namespace = "http://www.mediawiki.org/xml/export-0.8/"
fd = urllib.urlopen(url)
# Way 1)
#xmldata = fd.read()
#tree = ElementTree.fromstring(xmldata)
# Way 2)
tree = ElementTree()
tree.parse(fd)
root = tree.getroot()
print root.tag
#print root.attrib
#print root.keys()
#print root.items()
page_tag = str( QName( namespace, 'page' ) )
text_tag = str( QName( namespace, 'text' ) )
title_tag = str( QName( namespace, 'title' ) )

page = root.find(page_tag)
print page.find(text_tag)
for i in page.iter():
	if i.tag==title_tag:
		print "$TITLE", i.text
		print "$TITLE", type(i.text)
	if i.tag==text_tag:
		print "$TEXT", i.text[:100]
