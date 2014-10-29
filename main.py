#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import os
import jinja2
import logging
from models import Employee
from google.appengine.ext import ndb
from webapp2_extras import sessions

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True)

def employee_key(username):
    return ndb.Key('Employee', username)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

class MainPage(BaseHandler):
    def get(self):
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render())

    def post(self):
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render())

class HomePage(BaseHandler):
    def get(self):
        user_values = {
            'username': self.session.get('username'),
            'first_name': self.session.get('first_name'),
            'last_name': self.session.get('last_name'),
            'is_admin': self.session.get('is_admin')
        }
        template = jinja_env.get_template("templates/homepage.html")
        self.response.write(template.render(user_values))

class RegisterAction(BaseHandler):
    def post(self):
        username = self.request.get('newusername')
        password = self.request.get('newpassword')
        first_name = self.request.get('fname')
        last_name = self.request.get('lname')

        if (username  and password and first_name and last_name):
            employee_query = Employee.query(ancestor=employee_key(username))
            employees = employee_query.fetch()

            if (not employees):
                    new_employee = Employee(parent=employee_key(username), login_name=username, password=password, first_name=first_name, last_name=last_name)
                    new_employee.put()
                    self.session['username'] = username
                    self.session['first_name'] = employees[0].first_name
                    self.session['last_name'] = employees[0].last_name
                    self.session['is_admin'] = employees[0].is_admin
                    self.redirect('/home')
            else:
                self.redirect('/')
        else:
            self.redirect('/')

class LoginAction(BaseHandler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        if (username and password):
            employee_query = Employee.query(Employee.login_name == username, Employee.password == password)
            employees = employee_query.fetch()

            if (employees):
                self.session['username'] = username
                self.session['first_name'] = employees[0].first_name
                self.session['last_name'] = employees[0].last_name
                self.session['is_admin'] = employees[0].is_admin
                self.redirect('/home')
            else:
                self.redirect('/')
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/register', RegisterAction),
    ('/login', LoginAction),
    ('/home', HomePage)
], debug=True, config=config)
