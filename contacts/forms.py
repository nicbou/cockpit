from contacts.models import *
from django import forms
from django.forms import ModelForm
from django.forms import widgets

class ContactAddForm(ModelForm):
	picture = forms.ImageField(widget=widgets.FileInput,required=False)
	class Meta:
		model = Contact
		exclude = ('company',)