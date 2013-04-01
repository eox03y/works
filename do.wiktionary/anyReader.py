import sys
import codecs
import urllib2 	
import zlib

class UrlZipReader:
	def __init__(self, _url):
		self._url = _url
		try:
			self.fp = urllib2.urlopen(self._url)
		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			return
		if self._url.endswith(".gz"):
			self.zip = zlib.decompressobj(wbits=31)
		elif self._url.endswith(".zip"):
			self.zip = zlib.decompressobj(wbits=15)
		else:
			self.zip = None
		 
	def read(self, size=16*1024):
		chunk = self.fp.read(size)
		print '##', size, len(chunk)
		print '##', chunk[:1024]
		print self.zip.unconsumed_tail
		if not self.zip:
			return chunk
		if self.zip.unconsumed_tail != '':
			return self.zip.decompress(self.zip.unconsumed_tail)
		if chunk != '':
			return self.zip.decompress(chunk)
		return ''		


def anyReader(fname, encoding='utf-8'):

	if fname == '-':
		fp = sys.stdin
	elif fname.startswith('http://') or fname.startswith('https://'):
		import urllib2 	
		try:
			fp = urllib2.urlopen(fname)
		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			return None
		if fname.endswith(".gz") or fname.endswith(".zip") or fname.endswith(".bz2"):
			return UrlZipReader(fname) 

	elif fname.endswith(".gz"):
		import gzip
		fp = gzip.open(fname, 'rb')
	elif fname.endswith(".bz2"):
		import bz2
		fp = bz2.BZ2File(fname, 'rb')
	else:
		fp = open(fname, 'rb')


	if encoding=='ascii':
		return fp
	else:
		reader = codecs.getreader(encoding)
		if fname == '-':
			sys.stdin = reader(fp)
		return reader(fp)

def anyWriter(fname, encoding='utf-8'):

	if fname == '-':
		fp = sys.stdout
	elif fname.endswith(".gz"):
		import gzip
		fp = gzip.open(fname, 'wb')
	elif fname.endswith(".bz2"):
		import bz2
		fp = bz2.BZ2File(fname, 'wb')
	else:
		fp = open(fname, 'wb')


	if encoding=='ascii':
		return fp
	else:
		writer = codecs.getwriter(encoding)
		if fname == '-':
			sys.stdout = writer(fp)
		return writer(fp)
