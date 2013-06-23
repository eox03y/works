import sys
import codecs
import urllib2 	
import zlib
import bz2
import io

# see https://code.google.com/p/feedparser/source/browse/feedparser/feedparser.py

class UrlZipReader:
	def __init__(self, _url):
		self._url = _url
		try:
			#self.fp = urllib2.urlopen(self._url)
			req = urllib2.Request(self._url)
			req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.37 Safari/537.36")
			#req.add_header("User-agent", "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4")
			req.add_header("Connection", "Keep-Alive")
			print req.headers
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
			self.zip = bz2.BZ2Decompressor()
			#self.zip = bz2.BZ2File(self.fp)
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
			return res	
		return ''		


def anyReader(fname, encoding='utf-8'):

	if fname == '-':
		fp = sys.stdin
	flds = fname.split('.')
	extName = flds[-1]

	isXml = extName=='xml' or (len(flds) > 2 and flds[-2]=='xml')

	if fname.startswith('http://') or fname.startswith('https://'):
		if extName=='gz' or extName=='zip' or extName=='bz2':
			return UrlZipReader(fname) 

		import urllib2 	
		try:
			req = urllib2.Request(fname)
			req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.37 Safari/537.36")
			fp = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			return None

	elif extName=='gz':
		import gzip
		fp = gzip.open(fname, 'rb')
	elif extName=='bz2':
		import bz2
		fp = bz2.BZ2File(fname, 'rb')
	else:
		fp = open(fname, 'rb')


	# for XML file, we do not decode string into unicode because xml.sax handles ByteStream.
	if encoding=='ascii' or isXml:
		print "NO CODECS"
		return fp
	else:
		print "CODECS", encoding
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

if __name__=='__main__':
	reader = anyReader(sys.argv[1])
	CHUNK = 100*1024
	cnt = 0
	for chunk in iter(lambda: reader.read(CHUNK), ''):
		print 'READ', len(chunk)
		#print chunk
		cnt += len(chunk)

	print 'SUM', cnt

