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


class PageReadBlob(webapp.RequestHandler):
 def get(self):
	if not users.get_current_user():
		self.redirect('/2')
	else:
		blob_key = 'AMIfv963fCb95iLosF2vyEFz6HRVOsCMGlij-t4EzNiRyg6Or7q4N9NeddqWT0wlmmjD2C51PJJD85Tz9NLyUa1OzhSpL7Dg4v-G4rzkF7wzsz-zHhJqZKLYWLeH2URIXn8dfAHbQ12UZ_OqHJnwI9AreQ_8gKhNleHz-WH-ts2fnxw1zSmnazU'
		blob_reader = blobstore.BlobReader(blob_key)
		data = blob_reader.read(1000)
		html = ''
		html += '<html><body> user=%s <br/>' % (users.get_current_user().email())
		html += data.replace('\n', '<br/>')
		html += '</body></html>'
		self.response.out.write(html)

class UploadFormHandler(webapp.RequestHandler):
 def get(self):
	if users.get_current_user().nickname() != 'handol':
		self.redirect('/2')
		#url = users.create_login_url(self.request.uri)
		#url_linktext = 'Login'
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
                 self.redirect('/new')

         except:
              logging.error('Error in prosessing the file')
         self.response.out.write('Error in prosessing the file')

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

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


class Page3(webapp.RequestHandler):
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
	('/new', UploadFormHandler),
	('/upload', FileUploadHandler),
	('/', Page3),
	('/2', Page2),
	('/read', PageReadBlob),
	('/sign', Guestbook)
	],
	debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
