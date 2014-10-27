from google.appengine.ext import ndb

# TODO: Implement
class Employee(ndb.Model):
	""" Information for a user. """
	login_name = ndb.StringProperty()
 	password = ndb.StringProperty()
 	first_name = ndb.StringProperty()
 	last_name = ndb.StringProperty()
 	is_admin = ndb.BooleanProperty(default=False)