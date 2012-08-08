from projects.models import *
from django import forms
from django.forms import ModelForm
import django.contrib.auth 

#For forms with the "Project" field still present
class ModelAddForm(ModelForm):
	def __init__(self, company_id, *args, **kwargs):
		super(ModelAddForm, self).__init__(*args, **kwargs)
		#Only propose active projects that belong to this user
		self.fields['project'].queryset = Project.objects.filter(company_id=company_id).exclude(status=0).extra(order_by=['title'])

#Add/edit a project
class ProjectForm(ModelForm):
	class Meta:
		model = Project
		exclude = ('company',)

#Add/edit a memo
class MemoForm(ModelForm):
	class Meta:
		model = Memo
		exclude = ('project',)

#Add a memo to an arbitrary project
class MemoAddForm(ModelAddForm):
	class Meta:
		model = Memo
		
#Add/edit a document
class DocumentForm(ModelForm):
	class Meta:
		model = Document
		exclude = ('project',)

#Add a document to an arbitrary project
class DocumentAddForm(ModelAddForm):
	class Meta:
		model = Document

#Edit a document
class DocumentEditForm(ModelForm):
	class Meta:
		model = Document
		exclude = ('project','file',)

#Email a document
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

#Add/edit a task		
class TaskForm(ModelForm):
	class Meta:
		model = Task
		exclude = ('project','status')

#Add a task to an arbitrary project
class TaskAddForm(ModelAddForm):
	class Meta:
		model = Task