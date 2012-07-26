from accounts.models import *
from accounts.forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth import logout
from django.contrib.sites.models import Site

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


def signup(request):
	if request.POST:
		signup_form = SignUpForm(request.POST)
		if signup_form.is_valid():
			new_profile = signup_form.save()

			current_site = Site.objects.get_current()
			subject = "Activate your Cockpit account"
			message = "To activate your account, visit " + HttpRequest.build_absolute_uri(request,reverse('accounts.views.activate_account',args=[new_profile.user.id,new_profile.get_activation_key()]))
			from_email = 'contact@nicolasbouliane.com'
			to_emails = [new_profile.user.email]

			send_mail(subject, message, from_email, to_emails, fail_silently=False)
			return HttpResponseRedirect(reverse('accounts.views.signup_thankyou'))
	else:
		signup_form = SignUpForm()
		
	return render(request,"user_signup.html",{
		'signup_form' : signup_form,
	})

def signup_thankyou(request):
	return render(request,"user_signup_done.html")

def activate_account(request,user_id,key):
	user = User.objects.get(id=user_id)
	profile = user.get_profile()

	activated = False
	if profile.get_activation_key() == key:
		profile.user.is_active = True
		profile.user.save()
		activated = True
		login_form = LoginForm()

	return render(request,"user_signup_complete.html",{
		'activated':activated,
		'login_form':login_form,
	})