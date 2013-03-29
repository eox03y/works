import codecs
import sys

import anyReader
reader = anyReader.anyReader(sys.argv[1], 'ascii')
writer = anyReader.anyWriter(sys.argv[2], 'ascii')

##  failed
#from xml.dom import minidom
#xmldoc = minidom.parse(reader)
#for node in xmldoc:
#	writer.write('%s\n' % node.name)
	

## failed
#import xml.etree.ElementTree as ET
#tree = ET.parse(sys.argv[1])
#root = tree.getroot()
#print root

#import xml.sax
#xml.sax.parse(sys.argv[1], handler)

#
#import xml.sax
#xmlreader = xml.sax.make_parser()
#xmlreader.parse(sys.argv[1])


'''
python wik_xml_read.py enwiktionary-20130313-pages-meta-current.5000.xml a

  File "/usr/lib/python2.7/xml/sax/handler.py", line 38, in fatalError
    raise exception
xml.sax._exceptions.SAXParseException: enwiktionary-20130313-pages-meta-current.5000.xml:5001:0: no element found
'''
