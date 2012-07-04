from models import *
from django import forms
from django.forms import ModelForm

class UserProfileForm(ModelForm):
	class Meta:
		model = User
		fields=('first_name', 'last_name', 'email')