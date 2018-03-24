from __future__ import unicode_literals
from django.db import models
from ..main.models import *

class UserManager(models.Manager):
	def validateQuote(self, postData):
		print "VALIDATE ME!"

		result = {
			 'status': False,
			 'errors': None
		}

		errors = []

		if len(postData['author']) <= 3:
		 	errors.append("Author's name is too short.")
		if len(postData['quote']) <= 10:
		 	errors.append("The quote is too short.")

		if len(errors):
			result['errors'] = errors

		else:
			result['status'] = True
			user = Quote.objects.create(author = postData['author'],quote = postData['quote'],user = User.objects.get(id=int(postData['id'])))
			result['user_id'] = user.id

		print result
		return result

class Quote(models.Model):
	author = models.CharField(max_length=255)
	quote = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User,related_name='submissions')
	favr_id = models.ManyToManyField(User,related_name='favorites')
	objects = UserManager()
	def __str__(self):
		return self.author