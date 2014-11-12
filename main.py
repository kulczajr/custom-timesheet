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
import json
from models import Employee
from models import Position
from models import Timesheet
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
        if (self.session.get('username')):
            user_values = {
                'username': self.session.get('username'),
                'first_name': self.session.get('first_name'),
                'last_name': self.session.get('last_name'),
                'is_admin': self.session.get('is_admin')
            }
            template = jinja_env.get_template("templates/homepage.html")
            self.response.write(template.render(user_values))
        else:
            template = jinja_env.get_template("templates/mainpage.html")
            self.response.write(template.render())

    def post(self):
            template = jinja_env.get_template("templates/mainpage.html")
            self.response.write(template.render())

class HomePage(BaseHandler):
    def get(self):
        if (self.session.get('is_admin')):
            self.redirect('/adminLoad')
        else:
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
                    new_employee = Employee(parent=employee_key(username), login_name=username, password=password, first_name=first_name, last_name=last_name, positions=[])
                    new_employee.put()
                    self.session['username'] = username
                    self.session['first_name'] = first_name
                    self.session['last_name'] = last_name
                    self.session['is_admin'] = False
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
                employees = employees[0]
                self.session['username'] = username
                self.session['first_name'] = employees.first_name
                self.session['last_name'] = employees.last_name
                self.session['is_admin'] = employees.is_admin
                self.redirect('/home')
            else:
                self.redirect('/')
        else:
            self.redirect('/')

class LogoutAction(BaseHandler):
    def get(self):
        self.session.clear()
        self.redirect('/')

class adminLoginAction(BaseHandler):
    def get(self):
        employee_query = Employee.query(Employee.login_name != self.session.get('username'))
        employee_list = employee_query.fetch()

        position_query = Position.query()
        position_list = position_query.fetch()

        admin_values = {
            'username': self.session.get('username'),
            'first_name': self.session.get('first_name'),
            'last_name': self.session.get('last_name'),
            'is_admin': self.session.get('is_admin'),
            'positions': self.session.get('positions'),
            'employee_list': employee_list,
            'position_list': position_list
        }
        template = jinja_env.get_template("templates/admin_home.html")
        self.response.write(template.render(admin_values))

class adminEditAction(BaseHandler):
    def get(self):
        employee_query = Employee.query(Employee.login_name != self.session.get('username'))
        employee_list = employee_query.fetch()

        position_query = Position.query()
        position_list = position_query.fetch()

        admin_values = {
            'username': self.session.get('username'),
            'first_name': self.session.get('first_name'),
            'last_name': self.session.get('last_name'),
            'is_admin': self.session.get('is_admin'),
            'positions': self.session.get('positions'),
            'employee_list': employee_list,
            'position_list': position_list
        }
        template = jinja_env.get_template("templates/admin_edit.html")
        self.response.write(template.render(admin_values))

class createPositionAction(BaseHandler):
    def post(self):
        title = self.request.get('title')
        position_query = Position.query(Position.title == title)
        positions = position_query.fetch()

        if (len(positions) > 0):
            self.response.write(False)
        else:
            new_position = Position(title=title)
            new_position.put()
            self.response.write(True)

class retrievePositionsAction(BaseHandler):
    def post(self):
        employee_query = Employee.query(Employee.login_name == self.request.get('username'))
        employee = employee_query.fetch()[0]

        position_query = Position.query()
        positions = position_query.fetch()
        notUserTitles = []
        userTitles = []
        for position in positions:
            if position.key in employee.positions:
                userTitles.append(position.title)
            else:
                notUserTitles.append(position.title)

        titles = [notUserTitles, userTitles]

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(titles))

class addPositionAction(BaseHandler):
    def post(self):
        employee_query = Employee.query(Employee.login_name == self.request.get('username'))
        employee = employee_query.fetch()[0]

        position_query = Position.query(Position.title == self.request.get('position'))
        position = position_query.fetch()[0]
        employee.positions.append(position.key)
        employee.put()
        
        position_query = Position.query()
        positions = position_query.fetch()
        notUserTitles = []
        userTitles = []
        for position in positions:
            if position.key in employee.positions:
                userTitles.append(position.title)
            else:
                notUserTitles.append(position.title)

        titles = [notUserTitles, userTitles]

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(titles))

class removePositionAction(BaseHandler):
    def post(self):
        employee_query = Employee.query(Employee.login_name == self.request.get('username'))
        employee = employee_query.fetch()[0]

        position_query = Position.query(Position.title == self.request.get('position'))
        position = position_query.fetch()[0]
        employee.positions.remove(position.key)
        employee.put()

        position_query = Position.query()
        positions = position_query.fetch()
        notUserTitles = []
        userTitles = []
        for position in positions:
            if position.key in employee.positions:
                userTitles.append(position.title)
            else:
                notUserTitles.append(position.title)

        titles = [notUserTitles, userTitles]

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(titles))

class retrieveTimesheet(BaseHandler):
    def post(self):
        if (self.request.get('username')):
            user = self.request.get('username')
        else:
            user = self.session['username']
        employee_query = Employee.query(Employee.login_name == user)
        employee = employee_query.fetch()[0]

        timesheet_query = Timesheet.query(Timesheet.time_period == self.request.get('time_period'), Timesheet.worked_by == employee.key)
        timesheet = timesheet_query.fetch()

        currentPositions = []
        for sheet in timesheet:
            currentPositions.append(sheet.position)

        for position in employee.positions:
            if position not in currentPositions:
                new_timesheet = Timesheet(worked_by=employee.key, position=position, time_period=self.request.get('time_period'))
                new_timesheet.put()
                timesheet.append(new_timesheet)

        jsonSheet = {'sheets': []}
        for t in timesheet:
            obj = {
                'worked_by': Employee.query(Employee.key == t.worked_by).fetch()[0].login_name,
                'position': Position.query(Position.key == t.position).fetch()[0].title,
                'hours_worked': t.hours_worked,
                'time_period': t.time_period,
                'is_submitted': t.is_submitted,
                'is_approved': t.is_approved
            }
            jsonSheet['sheets'].append(obj)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(jsonSheet))

class saveTimesheetAction(BaseHandler):
    def post(self):
        employee_query = Employee.query(Employee.login_name == self.session['username'])
        employee = employee_query.fetch()[0]

        data = self.request.get_all('hours')
        data = [data[i:i+8] for i in range(0, len(data), 8)]

        for i in range(0, len(data)):
            position_query = Position.query(Position.title == data[i][0])
            position = position_query.fetch()[0]

            timesheet_query = Timesheet.query(Timesheet.time_period == self.request.get('week'), Timesheet.worked_by == employee.key, Timesheet.position == position.key)
            timesheet = timesheet_query.fetch()[0]

            del data[i][0]
            timesheet.hours_worked = map(int, data[i])
            timesheet.put()

class retrieveAdminTableAction(BaseHandler):
    def post(self):
        employee_query = Employee.query(Employee.is_admin == False)
        employees = employee_query.fetch()

        employeeKeys = []
        for employee in employees:
            employeeKeys.append(employee.key)

        timesheet_query = Timesheet.query(Timesheet.time_period == self.request.get('time_period'), Timesheet.worked_by.IN(employeeKeys))
        timesheets = timesheet_query.fetch()

        employeeList = []
        for employee in employees:
            is_submitted = False
            is_approved = False
            hours = 0

            for timesheet in timesheets:
                if timesheet.worked_by == employee.key:
                    is_submitted = timesheet.is_submitted
                    is_approved = timesheet.is_approved
                    hours += sum(timesheet.hours_worked)

            employeeList.append({
                'username': employee.login_name, 
                'first_name': employee.first_name, 
                'last_name': employee.last_name,
                'is_submitted': is_submitted,
                'is_approved': is_approved,
                'hours': hours
            })

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(employeeList))

class approveTimesheetAction(BaseHandler):
    def post(self):
        employee_query = Employee.query(Employee.login_name == self.request.get('username'))
        employee = employee_query.fetch()[0]

        timesheet_query = Timesheet.query(Timesheet.time_period == self.request.get('time_period'), Timesheet.worked_by == employee.key)
        timesheets = timesheet_query.fetch()

        for timesheet in timesheets:
            timesheet.is_approved = True
            timesheet.put()

class submitTimesheetAction(BaseHandler):
    def post(self):
        employee_query = Employee.query(Employee.login_name == self.request.get('username'))
        employee = employee_query.fetch()[0]

        timesheet_query = Timesheet.query(Timesheet.time_period == self.request.get('time_period'), Timesheet.worked_by == employee.key)
        timesheets = timesheet_query.fetch()

        for timesheet in timesheets:
            timesheet.is_submitted = True
            timesheet.put()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/register', RegisterAction),
    ('/login', LoginAction),
    ('/logout', LogoutAction),
    ('/home', HomePage),
    ('/createPosition', createPositionAction),
    ('/adminLoad', adminLoginAction),
    ('/adminEdit', adminEditAction),
    ('/retrievePositions', retrievePositionsAction),
    ('/removePosition', removePositionAction),
    ('/addPosition', addPositionAction),
    ('/retrieveTimesheet', retrieveTimesheet),
    ('/saveTimesheet', saveTimesheetAction),
    ('/retrieveAdminTable', retrieveAdminTableAction),
    ('/approveTimesheet', approveTimesheetAction),
    ('/submitTimesheet', submitTimesheetAction)
], debug=True, config=config)
