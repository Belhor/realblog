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
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)





class Post(db.Model):
	title = db.StringProperty(required = True)
	post = db.TextProperty(required = True)
	created = db.DateProperty(auto_now_add = True)

class HomePage(webapp2.RequestHandler):
 
    def get(self):
    	title = self.request.get("subject")
    	post = self.request.get("content")
    	posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
    	template_values ={ 'title':title, 'post':post, 'error':error,}
    	template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
    
    

class NewPost(MainHandler):
	def get(self):
		self.render("form.html")
	
	def post(self):
    	title = self.request.get("subject")
    	post = self.request.get("content")
    	if post and title:
    		p = Post(title=title, post = post)
    		p.put()
    		self.redirect("/blog/")
    	else:
    		error = "Please enter the title and the post!"
    		template_values ={ "title":title, "post":post, "error":error,}

app = webapp2.WSGIApplication([
    ('/blog/', HomePage),
    ('/blog/newpost/', NewPost)
], debug=True)
