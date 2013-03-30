import codecs
import sys

import anyReader
reader = anyReader.anyReader(sys.argv[1], 'ascii')
writer = anyReader.anyWriter(sys.argv[2], 'ascii')

import xml.sax
import xml.sax.handler

import re

srch_wik_head1 = re.compile(r'(=+)([^=]+)=+')
srch_wik_head2 = re.compile(r'====([^=]+)====')
srch_wik_head3 = re.compile(r'=====([^=]+)=====')

skip_title_prefixes = [
    'User:',
    'User ',
    'Wiktionary:'
]

skip_head_names = [
    'Etymology',
    'Translations',
    'Wiktionary:'
]

def wiki2dict(titleContent, textContent)
    '''
    parse text of 'text element' in 'wiktionary xml file'.
    '''
    for pf in skip_title_prefixes:
        if titleContent.startswith(pf): 
            return None

    isSkip = False
    for line in textContent.splitlines():
        if isSkip: continue
        m = srch_wik_head2.search(line)
        if m:
            print "##RE", m.group(0), m.group(1)
            if m.group(1) in skip_head_names:
                isSkip =  True
            else:
                isSkip =  False
        if not isSkip:
            print line

class WikXmlErrorHandler(xml.sax.handler.ErrorHandler):
    def error(self, exception):
        print exception.getMessage()
        print exception

    def fatalError(self, exception):
        print exception.getMessage()
        print exception

    def warning(self, exception):
        print exception.getMessage()

class WikXmlHandler(xml.sax.handler.ContentHandler):
    def __init__ (self):
        self.isPageElement = False
        self.isTitleElement = False
        self.titleContent = u""
        self.isTextElement = False
        self.textContent = u""

    def startElement(self, name, attrs):
        if name == 'page':
            self.isPageElement = True
        elif name == 'title':
            self.isTitleElement = True
            self.titleContent = ""
        elif name == 'text':
            self.isTextElement = True
            self.textContent = ""

    def endElement(self, name):
        if name == 'page':
            self.isPageElement= False
            print "###TITLE"
            print self.titleContent 
            #print "###TEXT"
            #print self.textContent
            wiki2dict(self.titleContent, self.textContent)
            self.titleContent = ""
            self.textContent = ""
        elif name == 'title':
            self.isTitleElement= False
        elif name == 'text':
            self.isTextElement = False

    def characters (self, ch):
        if self.isTitleElement:
            self.titleContent += ch
        elif self.isTextElement:
            self.textContent += ch

## Ways to construct a XMLReader object
# simple way: 
xmlreader = xml.sax.make_parser()
# good way:
# but, failed:  we have to implement parse()
# refer: http://docs.python.org/2/library/xml.sax.reader.html#module-xml.sax.xmlreader
#xmlreader = xml.sax.xmlreader.XMLReader()
# better way: IncrementalParser.feed(data), close(, reset()
#xmlreader = xml.sax.xmlreader.IncrementalParser()

# Set UTF-8 stdout in case of the user piping our output
#reload(sys)
#sys.setdefaultencoding('utf-8')
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

xmlreader.setContentHandler(WikXmlHandler())
xmlreader.setErrorHandler(WikXmlErrorHandler())
xmlreader.parse(sys.argv[1])



'''
python wik_xml_read.py enwiktionary-20130313-pages-meta-current.5000.xml a

  File "/usr/lib/python2.7/xml/sax/handler.py", line 38, in fatalError
    raise exception
xml.sax._exceptions.SAXParseException: enwiktionary-20130313-pages-meta-current.5000.xml:5001:0: no element found
'''
