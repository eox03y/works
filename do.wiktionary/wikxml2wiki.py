# -*- coding: utf-8 -*-
import codecs
import sys
import anyReader
import xml.sax
import xml.sax.handler
import xml.parsers.expat
import re

class WikXmlErrorHandler(xml.sax.handler.ErrorHandler):
	def error(self, exception):
		print exception.getMessage()
		print exception

	def fatalError(self, exception):
		print exception.getMessage()
		print exception

	def warning(self, exception):
		print exception.getMessage()

class DefaultWiktionHandler:
	def tt_handler(self, title, text):
		print '@', title	
		print '$', text	

'''
input: wiktionary xml file, wiktionHandler class
	wiktionHandler.tt_handler()	 must be defined.
	xml : <page> <title> ~~~ </title> <text> ~~~~~~~~</text> </page>
output: simplified wiki format
'''
class WikXmlHandler(xml.sax.handler.ContentHandler):
	def __init__ (self, wiktionhandler=DefaultWiktionHandler()):
		self.isPageElement = False
		self.isTitleElement = False
		self.titleContent = u""
		self.isTextElement = False
		self.textContent = u""
		self.wiktionhandler = wiktionhandler

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
			self.wiktionhandler.tt_handler(self.titleContent, self.textContent)
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


def proc_xmlfile(xmlfile, outfile):
	## Ways to construct a XMLReader object
	xmlreader = xml.sax.make_parser()
	# Set UTF-8 stdout in case of the user piping our output
	reload(sys)
	sys.setdefaultencoding('utf-8')
	import codecs

	# xmlreader process 'byte stream' and assume the byte stream is utf-8.
	# so, we don't have to use 'codecs'. actually, we must not decode utf-8
	#infd = anyReader.anyReader(xmlfile, encoding='utf-8')
	infd = anyReader.anyReader(xmlfile, encoding='ascii')
	outfd = anyReader.anyWriter(outfile, encoding='ascii')

	xmlreader.setContentHandler(WikXmlHandler())
	xmlreader.setErrorHandler(WikXmlErrorHandler())

	# use feed()
	CHUNK = 100*1024
	for chunk in iter(lambda: infd.read(CHUNK), ''):
		#print "UNCOMPRESSED",len(chunk)
		#print chunk.decode('utf-8')
		try:
			xmlreader.feed(chunk)
		except EOFError:
			pass
			print exception
			#raise

if __name__=="__main__":
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	infile = sys.argv[1]
	outfile = sys.argv[2]
	proc_xmlfile(infile, outfile)
