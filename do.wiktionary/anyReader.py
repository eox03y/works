import sys
import codecs
import urllib2 	
import zlib
import bz2

# see https://code.google.com/p/feedparser/source/browse/feedparser/feedparser.py

class UrlZipReader:
	def __init__(self, _url):
		self._url = _url
		try:
			#self.fp = urllib2.urlopen(self._url)
			req = urllib2.Request(self._url)
			req.add_header("Connection", "Keep-Alive")
			#req.add_header("Connection", "Keep-Alive")
			self.fp = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			return
		print self.fp.info()
		print self.fp.getcode()

		if self._url.endswith(".gz"):
			self.zip = zlib.decompressobj(31)
		elif self._url.endswith(".bz2"):
			#self.zip = bz2.BZ2Decompressor()
			self.fp = bz2.BZ2File(self.fp)
			self.zip = None
		elif self._url.endswith(".zip"):
			self.zip = zlib.decompressobj(15)
		else:
			self.zip = None
		 
	def read(self, size=16*1024):
		chunk = self.fp.read(size)
		print '##', size, len(chunk)
		#print '##', chunk[:1024].decode('utf-8')
		if not self.zip:
			return chunk
		if hasattr(self.zip, 'unconsumed_tail') and  self.zip.unconsumed_tail != '':
			#print self.zip.unconsumed_tail
			return self.zip.decompress(self.zip.unconsumed_tail)
		if chunk != '':
			res = self.zip.decompress(chunk)
			print "DEFLATE", len(res)
			if len(res)==0:
				res = bz2.decompress(chunk)
				print "DEFLATE", len(res)
			return res	
		return ''		


def anyReader(fname, encoding='utf-8'):

	if fname == '-':
		fp = sys.stdin
	elif fname.startswith('http://') or fname.startswith('https://'):
		if fname.endswith(".gz") or fname.endswith(".zip") or fname.endswith(".bz2"):
			return UrlZipReader(fname) 

		import urllib2 	
		try:
			fp = urllib2.urlopen(fname)
		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			return None

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
