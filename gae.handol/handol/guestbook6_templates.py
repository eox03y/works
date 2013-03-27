import cgi
import os
import BeautifulSoup

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
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

    path = os.path.join(os.path.dirname(__file__), 'index.html')
	
	
    self.response.out.write(template.render(path, template_values))
    self.response.out.write( doit() )	
    
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

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook)],
                                     debug=True)

def main():
  run_wsgi_app(application)

import urllib

def doit():
	urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')
	fp = urllib.urlopen("http://jeenee-kr.appspot.com")
	html = fp.read()
	soup = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8")
	res = '<p> '
	for link in soup('a'):
		try:
			res += link['href']
		except:
			pass
	#return res + ' </p>'
	return "<p> I love you Jeein </p>"
	

if __name__ == "__main__":
  main()