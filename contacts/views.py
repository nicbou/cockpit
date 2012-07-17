from contacts.models import *
from contacts.forms import *
from projects.views import user_can_access_company
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect

@login_required()
def contact_list(request):
	company_id = request.user.get_profile().company.id
	contacts = Contact.objects.filter(company_id = company_id)
	
	PhoneNumberFormSet = inlineformset_factory(Contact, PhoneNumber, can_delete=False)
	EmailAddressFormSet = inlineformset_factory(Contact, EmailAddress, can_delete=False)    
	WebsiteFormSet = inlineformset_factory(Contact, Website, can_delete=False)    
	
	if request.POST:
		contact = Contact()
		contact_form = ContactAddForm(request.POST,request.FILES,instance=contact)
		phonenumber_formset = PhoneNumberFormSet(request.POST,prefix='phone',instance=contact)
		emailaddress_formset = EmailAddressFormSet(request.POST,prefix='address',instance=contact)
		website_formset = WebsiteFormSet(request.POST,prefix='address',instance=contact)

		if contact_form.is_valid() and phonenumber_formset.is_valid() and emailaddress_formset.is_valid() and website_formset.is_valid():
			new_contact = contact_form.save(commit=False)
			new_contact.company_id = company_id
			new_contact.save()
			phonenumber_formset.save()
			emailaddress_formset.save()
			website_formset.save()
			return HttpResponseRedirect(reverse('contacts.views.contact_list'))
	else:
		contact_form = ContactAddForm()
		phonenumber_formset = PhoneNumberFormSet(prefix='phone')
		emailaddress_formset = EmailAddressFormSet(prefix='address')
		website_formset = WebsiteFormSet(prefix='address')
	
	formset = PhoneNumberFormSet()
	return render(request,"contacts_index.html",{
		'contacts' : contacts,
		'contact_form' : contact_form,
		'phonenumber_formset' : phonenumber_formset,
		'emailaddress_formset' : emailaddress_formset,
		'website_formset' : website_formset,
		'formset' : formset,
	})
		
@login_required()
def contact_single(request,contact_id):
	contact = get_object_or_404(Contact,id=contact_id)
	
	if not user_can_access_company(request.user,contact.company_id):
		return HttpResponse("You are not allowed to access this",status=403)
	
	PhoneNumberFormSet = inlineformset_factory(Contact, PhoneNumber, can_delete=False)
	EmailAddressFormSet = inlineformset_factory(Contact, EmailAddress, can_delete=False)    
	WebsiteFormSet = inlineformset_factory(Contact, Website, can_delete=False)    
	
	if request.POST:
		contact_form = ContactAddForm(request.POST,request.FILES,instance=contact)
		phonenumber_formset = PhoneNumberFormSet(request.POST,prefix='phone',instance=contact)
		emailaddress_formset = EmailAddressFormSet(request.POST,prefix='address',instance=contact)
		website_formset = WebsiteFormSet(request.POST,prefix='website',instance=contact)

		if contact_form.is_valid() and phonenumber_formset.is_valid() and emailaddress_formset.is_valid() and website_formset.is_valid():
			contact_form.save()
			phonenumber_formset.save()
			emailaddress_formset.save()
			website_formset.save()
			return HttpResponseRedirect(reverse('contacts.views.contact_single',args=[contact_id]))
	else:
		contact_form = ContactAddForm(instance=contact)
		phonenumber_formset = PhoneNumberFormSet(instance=contact,prefix='phone')
		emailaddress_formset = EmailAddressFormSet(instance=contact,prefix='address')
		website_formset = WebsiteFormSet(instance=contact,prefix='website')
	
	formset = PhoneNumberFormSet()
	return render(request,"contact_single.html",{
		'contact' : contact,
		'contact_form' : contact_form,
		'phonenumber_formset' : phonenumber_formset,
		'emailaddress_formset' : emailaddress_formset,
		'website_formset' : website_formset,
		'formset' : formset,
	})

@login_required()
def contact_delete(request,document_id):
	contact = get_object_or_404(Contact,id=document_id)
	company_id = contact.company_id
	if user_can_access_company(request.user,company_id):
		contact.picture.delete()
		contact.delete()
		if request.is_ajax():
			return HttpResponse(status=200)
		else:
			return HttpResponseRedirect(reverse('contact_list'))
	else:
		return HttpResponse("You are not allowed to access this",status=403)
	
@login_required()
def phonenumber_delete(request,phonenumber_id):
	phonenumber = get_object_or_404(PhoneNumber.objects.select_related(),id=phonenumber_id)
	
	if user_can_access_company(request.user,phonenumber.contact.company_id):
		contact_id = phonenumber.contact_id
		phonenumber.delete()
		if request.is_ajax():
			return HttpResponse(status=200)
		else:
			return HttpResponseRedirect(reverse('contacts.views.contact_single',args=[contact_id]))
	else:
		return HttpResponse("You are not allowed to access this",status=403)
		
@login_required()
def emailaddress_delete(request,emailaddress_id):
	emailaddress = get_object_or_404(EmailAddress.objects.select_related(),id=emailaddress_id)
	
	if user_can_access_company(request.user,emailaddress.contact.company_id):
		contact_id = emailaddress.contact_id
		emailaddress.delete()
		if request.is_ajax():
			return HttpResponse(status=200)
		else:
			return HttpResponseRedirect(reverse('contacts.views.contact_single',args=[contact_id]))
	else:
		return HttpResponse("You are not allowed to access this",status=403)
		
@login_required()
def website_delete(request,website_id):
	website = get_object_or_404(Website.objects.select_related(),id=website_id)
	
	if user_can_access_company(request.user,website.contact.company_id):
		contact_id = website.contact_id
		website.delete()
		if request.is_ajax():
			return HttpResponse(status=200)
		else:
			return HttpResponseRedirect(reverse('contacts.views.contact_single',args=[contact_id]))
	else:
		return HttpResponse("You are not allowed to access this",status=403)