from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import urlfetch

import datetime
import json
import urllib2
import urllib

class Mesg(db.Model):
	mesg = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class StackTags(db.Model):
	tag = db.StringProperty(indexed=True)
	#count = db.IntergerProperty(int)
	#date = db.DateProperty(datetime.date, auto_now_add=True)
	count = db.ListProperty(int, default=[])
	date = db.ListProperty(datetime.date, default=[])

def get_stack_tags(i, gae=True):
	url = 'http://api.stackoverflow.com/1.1/tags?page=%d&pagesize=100' % (i)
	if gae:
		result = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'application/x-www-form-urlencoded'})
	else:
		result = urllib2.urlopen(url)
		res = result.result()
		from gzip import GzipFile
		result = GzipFile('', 'r', 0, StringIO(e)).read()
		
	res = json.loads(result)
	taglist = res['tags']
	for tag in taglist:
		name = tag['name']
		count = tag['count']
		one = StackTags.get_or_insert(name)
		one.count.append(count)
		one.date.append(datetime.date.today())

class MyCron(webapp.RequestHandler):
	def get(self):
		for i in range(10):
			get_stack_tags(i)
		m = Mesg()
		m.mesg = 'my cron haha'
		m.put()
		# do something

if __name__=='__main__':
	get_stack_tags(0, gae=False)
