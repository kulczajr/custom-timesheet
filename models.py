from google.appengine.ext import ndb

class Position(ndb.Model):
	title = ndb.StringProperty()

class Employee(ndb.Model):
	login_name = ndb.StringProperty()
	password = ndb.StringProperty()
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
	positions = ndb.KeyProperty(kind=Position, repeated=True)
	is_admin = ndb.BooleanProperty(default=False)

class Timesheet(ndb.Model):
	worked_by = ndb.KeyProperty(kind=Employee)
	position = ndb.KeyProperty(kind=Position)
	hours_worked = ndb.IntegerProperty(repeated=True)
	time_period = ndb.StringProperty()
	is_submitted = ndb.BooleanProperty(default=False)
	is_approved = ndb.BooleanProperty(default=False)