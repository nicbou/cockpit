from models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class UserProfileForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
	class Meta:
		model = User
		fields=('first_name', 'last_name', 'email')
		
class PasswordChangeForm(forms.Form):
	password1 = forms.CharField(label='New password',max_length=20, widget=forms.PasswordInput())
	password2 = forms.CharField(label='Repeat password',max_length=20, widget=forms.PasswordInput())
	
	def clean_password2(self):
		if self.cleaned_data.get('password1') and self.cleaned_data.get('password2') and self.cleaned_data['password1'] != self.cleaned_data['password2']:
			raise ValidationError("The new passwords don't match")
		return self.cleaned_data['password2']