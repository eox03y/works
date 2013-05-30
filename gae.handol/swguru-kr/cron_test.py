import datetime
import json
import urllib2
import urllib
import gzip
from StringIO import StringIO

def get_stack_tags(i, gae=True):
	url = 'http://api.stackoverflow.com/1.1/tags?page=%d&pagesize=100' % (i)
	if gae:
		result = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'application/x-www-form-urlencoded'})
	else:
		result = urllib2.urlopen(url)
		result = result.read()
		print type(result)
		result = gzip.GzipFile('', 'r', 0, StringIO(result)).read()
		print result
		
	res = json.loads(result)	
	taglist = res['tags']
	for tag in taglist:
		name = tag['name']
		count = tag['count']
		print name,count

if __name__=='__main__':
	get_stack_tags(0, gae=False)
