from accounts.models import *
from accounts.forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required()
def user_profile(request):
	if request.POST:
		profile_form = UserProfileForm(request.POST, instance=request.user)
		if profile_form.is_valid():
			profile_form.save()
			return HttpResponseRedirect(reverse('accounts.views.user_profile'))
	else:
		profile_form = UserProfileForm(instance=request.user)
	return render(request,"user_profile.html",{
		'profile_form' : profile_form,
	})