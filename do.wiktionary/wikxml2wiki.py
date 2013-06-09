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

class DefaultWikXmlTtHandler:
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
	def __init__ (self, wikxmltthandler=DefaultWikXmlTtHandler()):
		self.isPageElement = False
		self.isTitleElement = False
		self.titleContent = u""
		self.isTextElement = False
		self.textContent = u""
		self.wikxmltthandler = wikxmltthandler

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
			self.wikxmltthandler.tt_handler(self.titleContent, self.textContent)
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

''' define my own Title/Text handler '''
class WikXmlTtHandler:
	def __init__(self, outf):
		self.outf = outf
	def tt_handler(self, title, text):
		self.outf.write('@ %s\n' % (title))	
		self.outf.write('$ %s\n' % (text))	
'''
Process English Wiktionary
'''
class ProcWiktionary:
	def __init__(self):
		pass

	''' define my own Title/Text handler '''
	def tt_handler(self, title, text):
		self.outf.write('@ %s\n' % (title))	
		self.outf.write('$ %s\n' % (text))	

	def process(self, xmlfile, outfile):
		xmlreader = xml.sax.make_parser()
		# set outout 
		self.outf = anyReader.anyWriter(outfile, encoding='utf-8')
		mytthandler = self
		xmlreader.setContentHandler(WikXmlHandler(mytthandler))
		xmlreader.setErrorHandler(WikXmlErrorHandler())
		# set input
		# 	xmlreader process 'byte stream' and assume the byte stream is utf-8.
		# 	Actually,for XML, we must not set encoding='utf-8', but encoding='ascii' 
		infd = anyReader.anyReader(xmlfile, encoding='ascii')
		CHUNK = 100*1024
		for chunk in iter(lambda: infd.read(CHUNK), ''):
			#print chunk.decode('utf-8')
			try:
				xmlreader.feed(chunk)
			except EOFError:
				pass
				break
				#print exception
				#raise

if __name__=="__main__":
	#print sys.getdefaultencoding()
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	infile = sys.argv[1]
	outfile = sys.argv[2]
	procwik = ProcWiktionary()
	procwik.process(infile, outfile)
	#proc_xmlfile(infile, outfile)
