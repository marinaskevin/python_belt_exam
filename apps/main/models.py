from __future__ import unicode_literals
from django.db import models
import re, bcrypt, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]{2}')
PASSWORD_REGEX = re.compile(r'[a-zA-Z0-9 !\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~"]{8}')

class UserManager(models.Manager):
	def validateRegistration(self, postData):

		feedback = {
			'name': postData['name'],
			'alias': postData['alias'],
			'email': postData['email'],
			'dob': postData['dob']
		}

		result = {
			 'status': False
		}

		errors = []

		if len(postData['name']) < 1:
			errors.append('Please enter your name (2 or more letters only).')
			feedback["name"] = ""
		elif len(postData['name']) < 2:
			errors.append('Name must have least 2 characters.')
			feedback["name"] = ""
		elif not NAME_REGEX.match(postData['name']):
			errors.append('Name must be letters only.')
			feedback["name"] = ""
		if len(postData['alias']) < 1:
			errors.append('Please enter your alias (2 or more letters only).')
			feedback["alias"] = ""
		elif len(postData['alias']) < 2:
			errors.append('Alias must have least 2 characters.')
			feedback["alias"] = ""
		elif not NAME_REGEX.match(postData['alias']):
			errors.append('Alias must be letters only.')
			feedback["alias"] = ""
		if len(postData['email']) < 1:
			errors.append('Please enter an email.')
		elif not EMAIL_REGEX.match(postData['email']):
			errors.append('Invalid Email.')
		if User.objects.filter(email=postData['email']).count() > 0:
			errors.append('Account '+postData['email']+' is already registered.')
			feedback["email"] = ""
		if len(postData['password']) < 1:
			errors.append('Please enter a password (8 or more characters).')
		elif len(postData['cpassword']) < 1:
			errors.append('Please confirm your password.')
		elif not PASSWORD_REGEX.match(postData['password']):
			errors.append('Password must have 8 or more characters.')
		if postData['password'] != postData['cpassword']:
			errors.append('Passwords do not match.')
		if len(postData['dob']) < 1:
			errors.append('Invalid birthday.')
		else:
			birthday = datetime.datetime(*[int(item) for item in feedback['dob'].split('-')])

		if len(errors):
			result['errors'] = errors

		else:
			result['status'] = True
			pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name = postData['name'],alias = postData['alias'],email = postData['email'],dob = birthday,pw_hash = pw_hash)
			result['user_id'] = user.id

		result['feedback'] = feedback		

		print result
		return result

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	dob = models.DateTimeField()
	pw_hash = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	def __str__(self):
		return self.name