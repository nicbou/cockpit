from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
import binascii
import hashlib
import magic

from datetime import date

class Descriptible (models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True,help_text=mark_safe("This field supports <a target='_blank' href='http://en.wikipedia.org/wiki/Markdown'>Markdown</a>"))
	creation_date = models.DateField(auto_now_add=True)
	class Meta:
		abstract = True

class Company (models.Model):
	name = models.CharField(max_length=200)
	telephone = models.CharField(max_length=11)
	is_active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

class Project (Descriptible):
	company = models.ForeignKey(Company)
	deadline = models.DateField(blank=True,null=True)
	COMPLETED = 0
	HOLD = 1
	ACTIVE = 2
	IMPORTANT = 3
	STATUS_CHOICES = (
		(IMPORTANT, 'High priority'),
		(ACTIVE, 'Active'),
		(HOLD, 'On hold'),
		(COMPLETED, 'Completed'),
	)
	status = models.SmallIntegerField(choices=STATUS_CHOICES,default=ACTIVE)

	def time_left_days(self):
		return (self.deadline - date.today()).days

	def time_overdue_days(self):
		return Project.time_left_days(self) * -1
		
	def time_left_percent(self):
		return int((float((date.today() - self.creation_date).days) / (self.deadline - self.creation_date).days)*100)
		
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ['-status','title']
		
class Document (Descriptible):
	project = models.ForeignKey(Project)
	file = models.FileField(upload_to='documents')
	
	def auth_key(self):
		return hashlib.md5(str(self.creation_date.isoformat())).hexdigest()
		
	def is_image(self):
		from PIL import Image
		try:
			trial_image = Image.open(settings.MEDIA_ROOT + self.file.name)
			trial_image.verify()
			return True
		except IOError:
			return False
			
	def is_pdf(self):
		if self.mimetype() == 'application/pdf':
			return True
		else:
			return False
			
	def is_text(self):
		if self.mimetype().startswith('text/'):
			return True
		else:
			return False
		
	def mimetype(self):
		m = magic.Magic(mime=True)
		return m.from_file(settings.MEDIA_ROOT + self.file.name)
		
	def content(self):
		return self.file.read()
		
	class Meta:
		ordering = ['-creation_date','project']
	
class Memo (models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=200)
	content = models.TextField(help_text=mark_safe("This field supports <a target='_blank' href='http://en.wikipedia.org/wiki/Markdown'>Markdown</a>"))
	creation_date = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-date_modified','-creation_date','project']
	
class Task (Descriptible):
	project = models.ForeignKey(Project)
	deadline = models.DateField(blank=True,null=True)
	COMPLETED = 0
	HOLD = 1
	ACTIVE = 2
	IMPORTANT = 3
	STATUS_CHOICES = (
		(IMPORTANT, 'High priority'),
		(ACTIVE, 'Active'),
		(HOLD, 'On hold'),
		(COMPLETED, 'Completed'),
	)
	status = models.SmallIntegerField(choices=STATUS_CHOICES,default=ACTIVE)
	
	def time_left_days(self):
		return (self.deadline - date.today()).days

	def time_overdue_days(self):
		return Task.time_left_days(self) * -1
		
	def time_left_percent(self):
		return int((float((date.today() - self.creation_date).days) / (self.deadline - self.creation_date).days)*100)


	class Meta:
		ordering = ['-status','-deadline','project','-creation_date']