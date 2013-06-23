import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import memcache
from google.appengine.api import taskqueue

#import jinja2
#import webapp2

import logging
import datetime
import threading
import json

# our programming
from wiktionary import wikdict
from wiktionary import wiktion2json

'''
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])
'''

IS_READY = False
'''
DB Define
'''

class BlobFile(db.Model):
  blobname = db.StringProperty()
  blobkey = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

class ApiDict(webapp.RequestHandler):
 def get(self):
		word = self.request.get('w')
		jsondata = wiktion2json.get_word2json(word)
		jsonstr = json.dumps(jsondata)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(jsonstr)


class Dict(webapp.RequestHandler):
 def get(self):
		global IS_READY
		word = self.request.get('w')
		#data = memcache.get(word)
		data = None
		if not data and IS_READY:
			data = wikdict.lookup_dict(word)
			if data:
				memcache.add(word, data, 3600*12)
		if not data:
			data = '<div class="nores"> not found </div>'
		template_values = {}
		#template_values['search_result'] = data.decode('utf-8')
		template_values['search_result'] = data
		path = os.path.join(os.path.dirname(__file__), 'home.html')
		self.response.out.write(template.render(path, template_values))
		#template = JINJA_ENVIRONMENT.get_template('home.html')
		#self.response.write(template.render(template_values))

class UploadForm(webapp.RequestHandler):
 def get(self):
	if users.get_current_user().nickname() != 'handol':
		self.redirect('/2')
	else:
		upload_url = blobstore.create_upload_url('/upload')
		html = ''
		html += '<html><body>'
		html += "%s" % upload_url
		html += '<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url
		html += """Upload File: <input type="file" name="file"><br> <input type="submit"
		name="submit" value="Submit"> </form></body></html>"""
		self.response.out.write(html)

class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
 def post(self):
         try:
              upload_files = self.get_uploads('file')
              logging.info('File upload received %s.  File count=%d' % (upload_files[0].filename, len(upload_files)))
              if len(upload_files) > 0:
                 blob_info = upload_files[0]
                 logging.info('Blob stored key=%s ' % (blob_info.key()))
                 blobfile = BlobFile()
                 blobfile.blobkey = upload_files[0].key()
                 blobfile.blobname = upload_files[0].filename
                 blobfile.put()
	
                 self.redirect('/new')

         except:
              logging.error('Error in prosessing the file')
         self.response.out.write('Error in prosessing the file')


class Home(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(template.render(path, template_values))
    #template = JINJA_ENVIRONMENT.get_template('home.html')
    #self.response.write(template.render(template_values))

class EnQueue(webapp.RequestHandler):
	def get(self):
		# The default URL path for the default queue is: /_ah/queue/default
		taskqueue.add(queue_name='default') 
		self.response.out.write('<html>OK</html>')
    

application = webapp.WSGIApplication( [
	('/dict', Dict),
	('/api/dict', ApiDict),
	('/new', UploadForm),
	('/upload', FileUploadHandler),
	('/enq', EnQueue),
	('/', Home)
	],
	debug=True)

def main():
  run_wsgi_app(application)

def loadindex():
	global IS_READY
	logging.info('Loading index file starts')
	wikdict.prepare()
	logging.info('Loading index file finished')
	IS_READY = True

class LoadIndex(threading.Thread):
	def run(self):
		loadindex()
if __name__ == "__main__":  
  #loadindex()
  main()
