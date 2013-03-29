import sys
import codecs

def anyReader(fname, encoding='utf-8'):

	if fname == '-':
		fp = sys.stdin
	elif fname.startswith('http://') or fname.startswith('https://'):
		import urllib 	
		fp = urllib.urlopen(fname)
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
		return writer(fp)
