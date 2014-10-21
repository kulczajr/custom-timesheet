from google.appengine.ext import ndb

# TODO: Implement
class Employee(ndb.Model):
	""" Information for a user. """
	login_name = ndb.StringProperty()
 