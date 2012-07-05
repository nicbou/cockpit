from accounts.models import *
from accounts.forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

@login_required()
def user_profile(request):
	if request.POST:
		if 'profile_form' in request.POST:
			profile_form = UserProfileForm(request.POST, instance=request.user)
			if profile_form.is_valid():
				profile_form.save()
				return HttpResponseRedirect(reverse('accounts.views.user_profile'))
		else:
			profile_form = UserProfileForm(instance=request.user)
		
		if 'password_form' in request.POST:
			password_form = PasswordChangeForm(request.POST)
			if password_form.is_valid():
				request.user.set_password(password_form.cleaned_data['password1'])
				request.user.save()
				logout(request)
				return HttpResponseRedirect(reverse('accounts.views.user_profile')+'#password')
		else:
			password_form = PasswordChangeForm()
	else:
		profile_form = UserProfileForm(instance=request.user)
		password_form = PasswordChangeForm()
		
	return render(request,"user_profile.html",{
		'profile_form' : profile_form,
		'password_form' : password_form,
	})