from contacts.models import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required()
def contact_list(request):
	contacts = Contact.objects.filter(company_id = request.user.get_profile().company.id)
		
	return render(request,"contacts_index.html",{
		'contacts' : contacts,
	})
	
@login_required()
def contact_single(request):
	contacts = Contact.objects.filter(company_id = request.user.get_profile().company.id)
		
	return render(request,"contacts_index.html",{
		'contacts' : contacts,
	})