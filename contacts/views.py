from contacts.models import *
from contacts.forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
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
		contact_form = ContactAddForm(request.POST,instance=contact)
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
	return render(request,"contact_single.html",{
	})
