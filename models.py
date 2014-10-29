from google.appengine.ext import ndb

# TODO: Implement
class Employee(ndb.Model):
	""" Information for a user. """
	login_name = ndb.StringProperty()
 	password = ndb.StringProperty()
 	first_name = ndb.StringProperty()
 	last_name = ndb.StringProperty()
 	is_admin = ndb.BooleanProperty(default=False)

class Timesheet(ndb.Model):
 	id = ndb.IntegerProperty()
 	worked_by = ndb.KeyProperty(kind=Employee)
 	hours_worked = ndb.IntegerProperty(repeated=True)
 	time_period = ndb.StringProperty()
 	is_submitted = ndb.BooleanProperty()
 	is_approved = ndb.BooleanProperty()