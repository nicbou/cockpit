from models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth.models import User, UserManager
from django.core.mail import send_mail

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

class LoginForm(forms.Form):
	username = forms.CharField(label='Username',max_length=20)
	password = forms.CharField(label='Password',max_length=128, widget=forms.PasswordInput())


class SignUpForm(forms.Form):
	company_name = forms.CharField(label='Company name', required=True, max_length=200)

	first_name = forms.CharField(label='Your first name', required=True, max_length=30)
	last_name = forms.CharField(label='Your last name', required=True, max_length=30)

	username = forms.CharField(label='Username', required=True, max_length=30, help_text='You can create more accounts later', validators=[validate_slug])

	email = forms.EmailField(label='E-mail address', required=True)

	password1 = forms.CharField(label='Password', help_text='Use a long, unique password',max_length=20, widget=forms.PasswordInput())
	password2 = forms.CharField(label='Repeat password', required=True, max_length=20, widget=forms.PasswordInput())
	
	def clean_username(self):
		#Make sure the username is unique
		try:
			user = User.objects.get(username__iexact=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError('This username is already taken. Please choose another.')

	def clean_password2(self):
		if self.cleaned_data.get('password1') and self.cleaned_data.get('password2') and self.cleaned_data['password1'] != self.cleaned_data['password2']:
			raise ValidationError("The passwords don't match")
		return self.cleaned_data['password2']

	def save(self):
		new_user = User.objects.create_user(self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
		new_user.is_active = False
		new_user.save()

		new_company = Company.objects.create(name=self.cleaned_data['company_name'])
		new_company.is_active = False
		new_company.save()

		new_userprofile = UserProfile.objects.create(user=new_user,company=new_company)
		new_userprofile.save()
		return new_userprofile