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
from models import Employee
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/mainpage.html")
        self.response.write(template.render())

    def post(self):
        self.redirect('/home')

class HomePage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/homepage.html")
        self.response.write(template.render())

class LoginAction(webapp2.RequestHandler):
    def post(self):
        self.redirect('/home')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginAction),
    ('/home', HomePage)
], debug=True)
