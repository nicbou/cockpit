from django.db import models
from django.contrib.auth.models import User
from projects.models import *

class UserProfile (models.Model):
	user = models.OneToOneField(User)
	company = models.ForeignKey(Company)