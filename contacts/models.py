from django.db import models
from projects.models import *
from django.forms.models import inlineformset_factory


#Similar to Django's groups, but without the bloat
class Group(Descriptible):
	company = models.ForeignKey(Company) #The company who created this Contact, not the company this Contact works for
	
	
class Contact(models.Model):
	#Generic information
	company = models.ForeignKey(Company) #The company who created owns this instance, not the company this Contact works for
	creation_date = models.DateField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	
	#User information
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30, blank=True)
	title = models.CharField(max_length=255, blank=True)
	picture = models.ImageField(upload_to='contact_pictures', blank=True)
	
	notes = models.TextField(blank=True)
	
	groups = models.ManyToManyField(Group,blank=True)
	
	def phonenumbers(self):
		return PhoneNumber.objects.filter(Contact=self)

	def emailaddresses(self):
		return EmailAddress.objects.filter(Contact=self)
		
	#Returns the full name. Borrowed from Django's User model
	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()


#Phone number for a contact		
class PhoneNumber(models.Model):
	Contact = models.ForeignKey(Contact)
	number = models.CharField(max_length = 40)
	HOME = 0
	WORK = 1
	MOBILE = 2
	HOME_FAX = 3
	WORK_FAX = 4
	PAGER = 5
	OTHER = 6
	TYPE_CHOICES = (
		(HOME, 'Home'),
		(WORK, 'Work'),
		(MOBILE, 'Mobile'),
		(HOME_FAX, 'Fax (home)'),
		(WORK_FAX, 'Fax (work)'),
		(PAGER, 'Pager'),
		(OTHER, 'Other')
	)
	type = models.SmallIntegerField(choices=TYPE_CHOICES, default=MOBILE)
	
	
#Email for a contact		
class EmailAddress(models.Model):
	Contact = models.ForeignKey(Contact)
	email = models.CharField(max_length = 255)
	PERSONAL = 0
	WORK = 1
	OTHER = 2
	TYPE_CHOICES = (
		(PERSONAL, 'Personal'),
		(WORK, 'Work'),
		(OTHER, 'Other')
	)
	type = models.SmallIntegerField(choices=TYPE_CHOICES, default=PERSONAL)


#URLs for contacts
class Website(models.Model):
	Contact = models.ForeignKey(Contact)
	url = models.CharField('Website URL',max_length = 255)
	WEBSITE = 0
	SOCIAL = 1
	OTHER = 2
	TYPE_CHOICES = (
		(WEBSITE, 'Website'),
		(SOCIAL, 'Social media'),
		(OTHER, 'Other')
	)
	type = models.SmallIntegerField(choices=TYPE_CHOICES, default=WEBSITE)

