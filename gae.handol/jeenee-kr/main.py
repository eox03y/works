import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import logging
# our programming
import wikdict

'''
DB Define
'''
class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class BlobFile(db.Model):
  blobname = db.StringProperty()
  blobkey = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

class PageReadBlob(webapp.RequestHandler):
 def get(self):
		data = wikdict.lookup_dict('happiness')
		data += wikdict.lookup_dict('satify')
		html = ''
		html += '<html><body> <br/>' 
		html += data.replace('\n', '<br/>')
		html += '</body></html>'
		self.response.out.write(html)

class Dict(webapp.RequestHandler):
 def get(self):
		data = wikdict.lookup_dict(self.request.get('w'))
		html = '<html><body> <br/>' 
		html += data.replace('\n', '<br/>')
		html += '</body></html>'
		self.response.out.write(html)

class DictForm(webapp.RequestHandler):
 def get(self):
		html = ''
		html += '<html><body>'
		html += '<form action="/dict" method="GET">'
		html += """Search: <input type="text" name="w"><br> <input type="submit"
		name="submit" value="Submit"> </form></body></html>"""
		self.response.out.write(html)

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


class Page2(webapp.RequestHandler):
  def get(self):
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'url': url,
      'url_linktext': url_linktext
      }

    path = os.path.join(os.path.dirname(__file__), '2.html')
    self.response.out.write(template.render(path, template_values))


class Home(webapp.RequestHandler):
  def get(self):
    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(10)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'greetings': greetings,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), '3.html')
    self.response.out.write(template.render(path, template_values))
    
import datetime
class Guestbook(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()

    tstr = str( datetime.datetime.now() )
    greeting.content = tstr + '   ' + self.request.get('content')
    greeting.put()
    self.redirect('/')

application = webapp.WSGIApplication( [
	('/dict', Dict),
	('/dictform', DictForm),
	('/new', UploadForm),
	('/upload', FileUploadHandler),
	('/', Home),
	('/2', Page2),
	('/read', PageReadBlob),
	('/sign', Guestbook)
	],
	debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  wikdict.prepare()
  main()
