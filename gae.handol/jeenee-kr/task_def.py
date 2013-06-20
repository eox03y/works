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

from google.appengine.api import taskqueue

class MyTaskHandler(webapp.RequestHandler):
	def post(self):
		logging.info('MyTaskHandler')
		self.response.out.write('<html> Task OK </html>')

if __name__=='__main__':
	pass
