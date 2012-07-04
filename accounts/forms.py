from projects.models import *
from django import forms
from django.forms import ModelForm

class UserProfileForm(ModelForm):
    first_name = forms.CharField(label=_(u'Prénom'), max_length=30)
    last_name = forms.CharField(label=_(u'Nom'), max_length=30)

    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kw):
        super(UserProfileForm, self).save(*args, **kw)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()

    class Meta:
        model = UserProfile