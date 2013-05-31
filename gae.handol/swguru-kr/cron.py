from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import urlfetch

import datetime
import json
import urllib2
import urllib
import gzip
import logging
from StringIO import StringIO

class Mesg(db.Model):
	mesg = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class StackTags(db.Model):
	tag = db.StringProperty(indexed=True)
	count = db.IntegerProperty(int)
	date = db.DateProperty(datetime.date, auto_now_add=True)
	#count = db.ListProperty(int, default=[])
	#date = db.ListProperty(datetime.date, default=[])

def get_stack_tags(i, gae=True):
	url = 'http://api.stackoverflow.com/1.1/tags?page=%d&pagesize=100' % (i)
	if gae:
		result = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'application/x-www-form-urlencoded'})
		logging.info('urlfetch RESULT %d from %s' % (result.status_code, url))
		result = result.content
	else:
		result = urllib2.urlopen(url)
		result = result.read()
		result = gzip.GzipFile('', 'r', 0, StringIO(result)).read()
	logging.info(result[:250])
	#print result
	res = json.loads(result)
	taglist = res['tags']
	for tag in taglist:
		name = tag['name']
		count = tag['count']
		one = StackTags()
		one.tag = name
		one.count = count
		one.date = datetime.date.today()

		one.put()

class MyCron(webapp.RequestHandler):
	def get(self):
		for i in range(10):
			get_stack_tags(i)
			break

		m = Mesg()
		m.mesg = 'my cron haha'
		#m.put()

		self.response.out.write('<html> OK </html>')

if __name__=='__main__':
	get_stack_tags(0, gae=False)
