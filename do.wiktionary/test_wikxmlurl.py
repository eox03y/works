from xml.etree.ElementTree import ElementTree
import urllib
urllib.URLopener.version = (
	'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '
	'Gecko/20050609 Firefox/1.0.4')

url = 'http://en.wiktionary.org/wiki/Special:Export/lion'
fd = urllib.urlopen(url)
# Way 1)
#xmldata = fd.read()
#tree = ElementTree.fromstring(xmldata)
# Way 2)
tree = ElementTree()
tree.parse(fd)
root = tree.getroot()
print root.tag
print root.attrib
print tree.find('page')

