from google.appengine.ext import webapp
from google.appengine.ext import db

class Mesg(db.Model):
	mesg = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class MyCron(webapp.RequestHandler):
	def get(self):
		m = Mesg()
		m.mesg = 'my cron haha'
		m.put()
		# do something

