from django.db import models
from django.contrib.auth.models import User
from projects.models import *
import hashlib

class UserProfile (models.Model):
	user = models.OneToOneField(User)
	company = models.ForeignKey(Company)

	def get_activation_key(self):
		"""
		Creates a hash for the account activation key. This hash is then compared to the
		one sent to validate the account.

		Note: Django loses microsecond info while saving to the database. Therefore,
		the hash of the database date_joined is different from the object's date_joined.
		"""
		return hashlib.md5(self.user.username + self.user.email + str(self.user.date_joined.second) + str(self.user.date_joined.second)).hexdigest()