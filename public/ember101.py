#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import urllib
import logging
import webapp2
import datetime
import cgi

from webapp2_extras.routes import RedirectRoute
from webapp2_extras import jinja2
import json
from functools import wraps

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import users

class Contact(ndb.Model):
	first = ndb.StringProperty()
	last = ndb.StringProperty()
	avatar = ndb.StringProperty()

class User(ndb.Model):
	google_id = ndb.UserProperty()
	creation_date = ndb.DateTimeProperty(auto_now_add=True)
	creation_author = ndb.UserProperty()
	modification_date = ndb.DateTimeProperty(auto_now =True)
	modification_author = ndb.UserProperty()
	avatar = ndb.StringProperty()
	email = ndb.StringProperty()
	certification = ndb.StringProperty()
	level = ndb.StringProperty()

class Dive(ndb.Model):
	creation_date = ndb.DateTimeProperty(auto_now_add=True)
	creation_author = ndb.UserProperty()
	modification_date = ndb.DateTimeProperty(auto_now =True)
	modification_author = ndb.UserProperty()
	user = ndb.KeyProperty(User)
	max_depth = ndb.StringProperty()
	avg_depth = ndb.StringProperty()
	dive_date = ndb.DateTimeProperty()
	dive_duration = ndb.StringProperty()
	dive_coordinates = ndb.StringProperty()


HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

def jinja2_factory(app):
	j = jinja2.Jinja2(app)
	j.environment.filters.update({
        #'naturaldelta':naturaldelta,
        })
	j.environment.globals.update({
        # 'Post': Post,
        #'ndb': ndb, # could be used for ndb.OR in templates
        })
	return j

def user_protect(f):
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            return self.redirect(users.create_login_url(self.request.uri))
        return f(self, *args, **kwargs)
    return decorated_function

class BaseHandler(webapp2.RequestHandler):
	@webapp2.cached_property
	def jinja2(self):
	# Returns a Jinja2 renderer cached in the app registry.
		return jinja2.get_jinja2(factory=jinja2_factory)

	def render_response(self, _template, **context):
		# Renders a template and writes the result to the response.
		rv = self.jinja2.render_template(_template, **context)
		self.response.write(rv)
	# def handle_exception(self, exception, debug):
	# 	# Log the error.
	# 	logging.exception(exception)
	# 	# Set a custom message.
	# 	self.response.write("An error occurred.")
	# 	# If the exception is a HTTPException, use its error code.
	# 	# Otherwise use a generic 500 error code.
	# 	if isinstance(exception, webapp2.HTTPException):
	# 		self.response.set_status(exception.code)
	# 	else:
	# 		self.response.set_status(500)
	def render_error(self, message):
		logging.exception("Error 500: {0}".format(message))
		self.response.write("Error 500: {0}".format(message))
		return self.response.set_status(500)		



class RootHandler(BaseHandler):
	def get(self):
		user = users.get_current_user()
		if not user:
			user_url = users.create_login_url(self.request.uri)
			user_linktext = 'Sign in or Sign up'
			user_email = ''
		else:
			self.register_user(user)
			user_url = users.create_logout_url('/')
			user_linktext = 'Sign out'
			user_email = user.email()

		template_values = {
			'user_url': user_url,
			'user_linktext': user_linktext,
			'user_email': user_email,
		}	
		return self.render_response("main.html", **template_values)

	def register_user(self, user):
		user_test = User.query(User.google_id==user).fetch()
		if len(user_test) != 0:
			return
		new_user = User()
		new_user.google_id = user
		new_user.creation_author = user
		new_user.email = user.email()
		new_user.put()




class ContactsHandler(BaseHandler):
	def get(self):
		contacts = Contact.query().fetch()
		#logging.info(obj)
		obj = dict()
		obj['contacts'] = list()
		for contact in contacts:
			current = dict()
			current['id'] = contact.key.id()
			current['first'] = contact.first
			current['last'] = contact.last
			current['avatar'] = contact.avatar
			obj['contacts'].append(current)
		logging.info(obj)

		self.response.headers['Content-Type'] = 'application/json'   
		return self.response.out.write(json.dumps(obj))
		# return self.response.write('{"contacts":[{"id":"abcdefg","first":"Ryan","last":"Florence","avatar":"http://www.gravatar.com/avatar/749001c9fe6927c4b069a45c2a3d68f7.jpg"},{"id":"123456","first":"Stanley","last":"Stuart","avatar":"https://si0.twimg.com/profile_images/3579590697/63fd9d3854d38fee706540ed6611eba7.jpeg"},{"id":"1a2b3c","first":"Eric","last":"Berry","avatar":"https://si0.twimg.com/profile_images/3254281604/08df82139b53dfa4a3a5adfa7e99426e.jpeg"}]}')

	@user_protect
	def post(self):
		request = json.loads(cgi.escape(self.request.body))
		contact = Contact(first = request['contact']['first'],
						  last = request['contact']['last'],
						  avatar = request['contact']['avatar'])
		contact.put()
		# return self.redirect('/#/contacts/')

class ContactHandler(BaseHandler):
	def get(self, contact_id):
		contact.get_by_id(contact_id)

	def put(self, contact_id):
		request = json.loads(cgi.escape(self.request.body))
		contact = Contact.get_by_id(int(contact_id))
		contact.first = request['contact']['first']
		contact.last = request['contact']['last']
		contact.avatar = request['contact']['avatar']
		contact.put()

	def delete(self, contact_id):
		ndb.Key(Contact, int(contact_id)).delete()

class UsersHandler(BaseHandler):
	def get(self):
		users = User.query().fetch()
		#logging.info(obj)
		obj = dict()
		obj['users'] = list()
		for user in users:
			current = dict()
			current['id'] = user.key.id()
			current['creation_date'] = user.creation_date.strftime("%Y-%m-%d %H:%M:%S")
			#current['creation_author'] = user.creation_author.email
			current['modification_date'] = user.modification_date.strftime("%Y-%m-%d %H:%M:%S")
			#current['modification_author'] = user.modification_author.email
			current['avatar'] = user.avatar
			current['email'] = user.email
			current['certification'] = user.certification
			current['level'] = user.level
			obj['users'].append(current)
		logging.info(obj)

		self.response.headers['Content-Type'] = 'application/json'
		self.response.headers['Access-Control-Allow-Origin'] = '*'
		return self.response.out.write(json.dumps(obj))
		# return self.response.write('{"contacts":[{"id":"abcdefg","first":"Ryan","last":"Florence","avatar":"http://www.gravatar.com/avatar/749001c9fe6927c4b069a45c2a3d68f7.jpg"},{"id":"123456","first":"Stanley","last":"Stuart","avatar":"https://si0.twimg.com/profile_images/3579590697/63fd9d3854d38fee706540ed6611eba7.jpeg"},{"id":"1a2b3c","first":"Eric","last":"Berry","avatar":"https://si0.twimg.com/profile_images/3254281604/08df82139b53dfa4a3a5adfa7e99426e.jpeg"}]}')


	def post(self):
		request = json.loads(cgi.escape(self.request.body))
		user = User(email = request['user']['email'],
						  last = request['user']['last'],
						  avatar = request['user']['avatar'])
		user.put()
		# return self.redirect('/#/contacts/')

class UserHandler(BaseHandler):
	def get(self, user_id):
		user.get_by_id(user_id)

	def put(self, user_id):
		request = json.loads(cgi.escape(self.request.body))
		user = User.get_by_id(int(user_id))
		user.first = request['user']['first']
		user.last = request['user']['last']
		user.avatar = request['user']['avatar']
		user.put()

	def delete(self, user_id):
		ndb.Key(User, int(user_id)).delete()

class DivesHandler(BaseHandler):
	def get(self):
		dives = Dive.query().fetch()
		#logging.info(obj)
		obj = dict()
		obj['dive'] = list()
		for dive in dives:
			current = dict()
			current['id'] = dive.key.id()
			current['creation_date'] = dive.creation_date.strftime("%Y-%m-%d %H:%M:%S")
			#current['creation_author'] = dive.creation_author.email
			current['modification_date'] = dive.modification_date.strftime("%Y-%m-%d %H:%M:%S")
			#current['modification_author'] = dive.modification_author.email
			current['max_depth'] = dive.max_depth

			current['avg_depth'] = dive.avg_depth
			if (dive.dive_date):
				current['dive_date'] = dive.dive_date.strftime("%Y-%m-%d %H:%M:%S")
			current['dive_duration'] = dive.dive_duration
			current['dive_coordinates'] = dive.dive_coordinates
			obj['dive'].append(current)
		logging.info(obj)

		self.response.headers['Content-Type'] = 'application/json'
		self.response.headers['Access-Control-Allow-Origin'] = '*'
		return self.response.out.write(json.dumps(obj))
		# return self.response.write('{"contacts":[{"id":"abcdefg","first":"Ryan","last":"Florence","avatar":"http://www.gravatar.com/avatar/749001c9fe6927c4b069a45c2a3d68f7.jpg"},{"id":"123456","first":"Stanley","last":"Stuart","avatar":"https://si0.twimg.com/profile_images/3579590697/63fd9d3854d38fee706540ed6611eba7.jpeg"},{"id":"1a2b3c","first":"Eric","last":"Berry","avatar":"https://si0.twimg.com/profile_images/3254281604/08df82139b53dfa4a3a5adfa7e99426e.jpeg"}]}')
	def post(self):
		request = json.loads(cgi.escape(self.request.body))
		logging.info(request)
		dive = Dive()
		dive.max_depth = request['dive']['max_depth']
		dive.avg_depth = request['dive']['avg_depth']
		dive.dive_date = request['dive']['dive_date']
		dive.dive_duration = request['dive']['dive_duration']
		dive.dive_coordinates = request['dive']['dive_coordinates']
		dive.put()
		
		#current_user = users.get_current_user()
		#request = json.loads(cgi.escape(self.request.body))
		#user = User.query(User.google_id == current_user).fetch()
		#dive = Dive(user = user)
		#user.put()
		self.response.headers['Access-Control-Allow-Origin'] = '*'
		return self.response.set_status(200)
		# return self.redirect('/#/contacts/')
	def options(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.headers['Access-Control-Allow-Origin'] = '*'
		self.response.headers['Access-Control-Allow-Headers'] = 'accept, content-type'
		self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
		return self.response.set_status(200)


class DiveHandler(BaseHandler):
	def get(self, dive_id):
		dive.get_by_id(dive_id)

	def put(self, dive_id):
		request = json.loads(cgi.escape(self.request.body))
		user = Contact.get_by_id(int(dive_id))
		user.first = request['dive']['first']
		user.last = request['dive']['last']
		user.avatar = request['dive']['avatar']
		user.put()

	def delete(self, dive_id):
		ndb.Key(Dive, int(dive_id)).delete()
	def options(self, dive_id):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.headers['Access-Control-Allow-Origin'] = '*'
		self.response.headers['Access-Control-Allow-Headers'] = 'accept, content-type'
		self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE'
		return self.response.set_status(200)


class OAuth2Callback(BaseHandler):
	def get(self):
		logging.info(self.request)
		logging.info(self.request.get('access_token'))
		logging.info(self.request.get('token_type'))
		logging.info(self.request.get('expires_in'))
		logging.info(self.request.get('scope'))
		logging.info(self.request.get('authuser'))
		logging.info(self.request.get('num_sessions'))
		logging.info(self.request.get('session_state'))
		return self.response.set_status(200)
	def options(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.response.headers['Access-Control-Allow-Origin'] = '*'
		self.response.headers['Access-Control-Allow-Headers'] = 'accept, content-type'
		self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE'
		return self.response.set_status(200)
	def post(self):
		request = json.loads(cgi.escape(self.request.body))
		logging.info(request)
		return self.response.set_status(200)

class Root(BaseHandler):
	def get(self):
		return self.render_response('index.html')


application = webapp2.WSGIApplication([
	webapp2.Route(r'/', Root),
	webapp2.Route(r'/api/contacts', ContactsHandler, name='ContactsHandler'),
	webapp2.Route(r'/api/contacts/<dive_id:([^/]+)?>', ContactHandler, name='ContactHandler'),
	webapp2.Route(r'/api/users', UsersHandler),
	webapp2.Route(r'/api/users/<user_id:([^/]+)?>', UserHandler),
	webapp2.Route(r'/api/dives', DivesHandler),
	webapp2.Route(r'/api/dives/<dive_id:([^/]+)?>', DiveHandler),
	webapp2.Route(r'/oauth2callback', OAuth2Callback),

	], debug=True)