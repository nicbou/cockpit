from projects.models import *
from django import forms
from django.forms import ModelForm


class ProjectForm(ModelForm):
	class Meta:
		model = Project
		exclude = ('company',)

class MemoForm(ModelForm):
	class Meta:
		model = Memo
		exclude = ('project',)
		
class DocumentAddForm(ModelForm):
	class Meta:
		model = Document
		exclude = ('project',)
		
class DocumentEditForm(ModelForm):
	class Meta:
		model = Document
		exclude = ('project','file',)

class DocumentEmailForm(forms.Form):
	sender = forms.EmailField()
	recipients = forms.CharField(label="Recipients' emails")
	message = forms.CharField(widget=forms.Textarea)
	
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		document = kwargs.pop('document', None)
		public_url = kwargs.pop('public_url', None)
		super(DocumentEmailForm, self).__init__(*args, **kwargs)
		self.fields['sender'].initial = user.email
		self.fields['message'].initial = user.get_full_name() + " from " + user.get_profile().company.name + " wants to share the following document with you: " + public_url
		
class TaskForm(ModelForm):
	class Meta:
		model = Task
		exclude = ('project','status')