from contacts.models import *
from django import forms
from django.forms import ModelForm


class ContactAddForm(ModelForm):
	class Meta:
		model = Contact
		exclude = ('company',)