import codecs
import sys
from xml.dom import minidom

import anyReader
reader = anyReader.anyReader(sys.argv[1], 'ascii')
writer = anyReader.anyWriter(sys.argv[2], 'ascii')

##  failed
#xmldoc = minidom.parse(reader)
#for node in xmldoc:
#	writer.write('%s\n' % node.name)
	


import xml.etree.ElementTree as ET
tree = ET.parse(sys.argv[1])
root = tree.getroot()
print root


