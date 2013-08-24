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


#reIMG = re.compile(r'\[\[Image:([^\]]+)\]\]')
#reFILE = re.compile(r'\[\[File:([^\]]+)\]\]')
sample_lines = '''
[[File:Heterochromia.jpg|thumb|An example of ''heterochromia iridis'']]
[[File:June odd-eyed-cat.jpg|thumb|An [[w:odd-eyed cat|odd-eyed cat]], the result of heterochromia]]
'''

reIMG = re.compile(r'\[\[Image:([^\n]+)\n')
reFILE = re.compile(r'\[\[File:([^\n]+)\n')
def get_img_files(text):
	res = []
	res += [img for img in reIMG.findall(text)]
	res += [file for file in reFILE.findall(text)]
	return res

'''
input: wiktionary xml file, wiktionHandler class
	xml : <page> <title> ~~~ </title> <text> ~~~~~~~~</text> </page>
output: simplified wiki format
'''
class WikXmlHandler(xml.sax.handler.ContentHandler):
	def __init__ (self, outfd):
		self.ns = -1
		self.content = u''
		self.tagname = u''
		self.outfd = outfd

	def startElement(self, name, attrs):
		self.tagname = name
		self.content = u''

	def endElement(self, name):
		if name == 'page' and self.ns==0:
			res = get_img_files(self.textContent)
			if len(res) > 0:
				self.outfd.write('@ %s\n' % (self.titleContent))	
				for r in res:
					self.outfd.write('$ %s\n' % (r))

		elif name == 'title':
			self.titleContent = self.content
		elif name == 'text':
			self.textContent = self.content
		elif name == 'ns':
			self.ns = int(self.content)


	def characters (self, ch):
		self.content += ch

'''
Process English Wiktionary
'''
class ProcWiktionary:
	def __init__(self):
		pass

	def process(self, xmlfile, outfile):
		xmlreader = xml.sax.make_parser()
		# set outout 
		self.outf = anyReader.anyWriter(outfile, encoding='utf-8')
		xmlreader.setContentHandler(WikXmlHandler(self.outf))
		xmlreader.setErrorHandler(WikXmlErrorHandler())
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
	print get_img_files(sample_lines)	
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	infile = sys.argv[1]
	outfile = sys.argv[2]
	procwik = ProcWiktionary()
	procwik.process(infile, outfile)
	#proc_xmlfile(infile, outfile)
