from models import *
from django import forms
from django.forms import ModelForm

class UserProfileForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
	class Meta:
		model = User
		fields=('first_name', 'last_name', 'email')