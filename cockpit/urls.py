from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

	#Projects
	url(r'^$', 'projects.views.index', name='home'),
	url(r'^comments/delete/(\d+)$', 'projects.views.comment_delete', name='comment_delete'), 
	url(r'^documents$', 'projects.views.document_all', name='document_all'),
	url(r'^documents/(\d+)$', 'projects.views.document_single', name='document_single'),
	url(r'^documents/(\d+)/(.*)$', 'projects.views.document_single', name='document_public'),
	url(r'^documents/delete/(\d+)$', 'projects.views.document_delete', name='document_delete'),
	url(r'^memos/delete/(\d+)$', 'projects.views.memo_delete', name='memo_delete'), 
	url(r'^memos/edit/(\d+)$', 'projects.views.memo_edit', name='memo_edit'), 
	url(r'^projects/$', 'projects.views.index', name='project_list'),
	url(r'^projects/(\d+)$', 'projects.views.project_single', name='project_single'),
	url(r'^projects/delete/(\d+)$', 'projects.views.project_delete', name='project_delete'),
	url(r'^projects/(\d+)/(\d+)$', 'projects.views.project_status', name='project_status'),
	url(r'^tasks$', 'projects.views.task_all', name='task_all'),
	url(r'^projects/(\d+)/tasks$', 'projects.views.task_all'),
	url(r'^projects/(\d+)/documents$', 'projects.views.document_all'),
	url(r'^tasks/(\d+)/(\d+)$', 'projects.views.task_status', name='task_status'),
	(r'^comments/', include('django.contrib.comments.urls')),
	
	#Contacts
	url(r'^contacts$', 'contacts.views.contact_list', name='contact_list'),
	url(r'^contacts/(\d+)$', 'contacts.views.contact_single', name='contact_single'),
	url(r'^contacts/delete/(\d+)$', 'contacts.views.contact_delete', name='contact_delete'),
	url(r'^contacts/delete_phonenumber/(\d+)$', 'contacts.views.phonenumber_delete', name='phonenumber_delete'),
	url(r'^contacts/delete_emailaddress/(\d+)$', 'contacts.views.emailaddress_delete', name='emailaddress_delete'),
	url(r'^contacts/delete_website/(\d+)$', 'contacts.views.website_delete', name='website_delete'),
	
	#User profile
	(r'^profile/$', 'accounts.views.user_profile'),
	
	#Company profile
	#(r'^company/$', 'projects.views.company_profile'),
	
	#Login and registration
	(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'profile/login.html'}),
	(r'^login/reset/$', 'django.contrib.auth.views.password_reset',{'template_name': 'profile/password_reset_form.html','post_reset_redirect' : '/login/reset/done/'}),
	(r'^login/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',{'template_name': 'profile/password_reset_confirm.html','post_reset_redirect' : '/login/reset/complete/'}),
	(r'^login/reset/done/$', 'django.contrib.auth.views.password_reset_done',{'template_name': 'profile/password_reset_done.html'}),
	(r'^login/reset/complete/$', 'django.contrib.auth.views.password_reset_complete',{'template_name': 'profile/password_reset_complete.html'}),
	(r'^logout/$', 'projects.views.user_logout'),
	url(r'^signup/$', 'accounts.views.signup', name='signup'),
	url(r'^signup/thankyou$', 'accounts.views.signup_thankyou', name='signup_thankyou'),
	url(r'^signup/(\d+)/(.*)$', 'accounts.views.activate_account', name='activate_account'),
	
	#Static files and documents
	(r'^documents/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT + 'documents'}),
	(r'^files/contact_pictures/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT + 'contact_pictures'}),
	)