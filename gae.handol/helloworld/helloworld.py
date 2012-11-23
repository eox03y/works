import os
import cgi
import datetime
import webapp2
import jinja2

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
	
class MainPage2(webapp2.RequestHandler):
	def get(self):	   
		self.response.headers['Content-Type'] = 'text/plain'	   
		self.response.write('Hello, webapp2 World!')  


class MainPage(webapp2.RequestHandler):
	def get(self):
		guestbook_name=self.request.get('guestbook_name')
		greetings_query = Greeting.all().ancestor(
			guestbook_key(guestbook_name)).order('-date')
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

		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))



from google.appengine.ext import db
from google.appengine.api import users

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class MainPage3(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')

    greetings = db.GqlQuery("SELECT * "
                            "FROM Greeting "
                            "ORDER BY date DESC LIMIT 10")

    for greeting in greetings:
      if greeting.author:
        self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))


    self.response.out.write("""
          <form action="/sign" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
        </body>
      </html>""")


class UserName(webapp2.RequestHandler):
  def get(self):         
    user = users.get_current_user()
    if user:             
      greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" % (user.nickname(), users.create_logout_url("/")))
    else:             
      greeting = ("<a href=\"%s\">Sign in or register</a>." % users.create_login_url("/"))
    self.response.out.write("<html><body>%s</body></html>" % greeting)
	
class Guestbook(webapp2.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()
    
    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/name', UserName),
  ('/sign', Guestbook)
], debug=True)
		
