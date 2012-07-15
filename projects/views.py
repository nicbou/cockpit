from projects.models import *
from projects.forms import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import comments
from itertools import chain
import operator


@login_required()
def index (request):
	company_id = request.user.get_profile().company.id
	project_form = ProjectAddForm(prefix="project")
	if request.POST:
		project_form = ProjectAddForm(request.POST,prefix="project")
		if project_form.is_valid():
			new_project = project_form.save(commit=False)
			new_project.company_id = company_id
			new_project.save()
			return redirect('project_single', new_project.id)
	projects = Project.objects.filter(company_id = company_id).exclude(status = 0)
	tasks = Task.objects.filter(project__in = projects).exclude(status = 0)[:30]
	memos = Memo.objects.filter(project__in = projects)[:30]
	documents = Document.objects.filter(project__in = projects)[:30]
	
	recent = sorted(chain(tasks,documents), key=operator.attrgetter('creation_date'), reverse=True)[:10]
	return render(request,"index.html",{
		'projects' : projects,
		'tasks' : tasks,
		'memos' : memos,
		'documents' : documents,
		'project_form' : project_form,
	})

	
def user_can_access_company(user,company_id):
	if user.is_anonymous():
		return False
		
	try:
		profile = user.get_profile()
	except UserProfile.DoesNotExist:
		profile = UserProfile.objects.create(user=user,company_id=company_id)
		
	if profile.company_id == company_id:
		return True
	else:
		return False

		
def user_can_access_project(user,project_id):
	if user.is_anonymous():
		return False
		
	project = get_object_or_404(Project,id=project_id)
	profile = None
	try:
		profile = user.get_profile()
	except UserProfile.DoesNotExist:
		profile = UserProfile.objects.create(user=user,company=project.company)
	company = get_object_or_404(Company,id=profile.company_id)
	if project.company_id == company.id:
		return True
	else:
		return False

		
def user_logout(request):
    logout(request)
    return redirect('/')

    
@login_required()	
def project_single (request,project_id):
	project = get_object_or_404(Project,id=project_id)
	documents = Document.objects.filter(project_id=project_id)
	memos = Memo.objects.filter(project_id=project_id)
	tasks = Task.objects.filter(project_id=project_id).exclude(status=Task.COMPLETED)
	
	if not user_can_access_project(request.user,project_id):
		return HttpResponse("You are not allowed to access this",status=403)

	if request.POST:
		if 'document_form' in request.POST:
			document_form = DocumentAddForm(request.POST, request.FILES, prefix="document")
			if document_form.is_valid():
				new_document = document_form.save(commit=False)
				new_document.project_id = project_id
				new_document.save()
				return HttpResponseRedirect(reverse('projects.views.project_single',args=[project_id]) + "#documents")
		else:
			document_form = DocumentAddForm(prefix="document")	

		if 'memo_form' in request.POST:
			memo_form = MemoAddForm(request.POST, prefix="memo")
			if memo_form.is_valid():
				new_memo = memo_form.save(commit=False)
				new_memo.project_id = project_id
				new_memo.save()
				memo_form = MemoAddForm(prefix="memo")
				return HttpResponseRedirect(reverse('projects.views.project_single',args=[project_id]) + "#memos")
		else:
			memo_form = MemoAddForm(prefix="memo")
			
		if 'task_form' in request.POST:
			task_form = TaskAddForm(request.POST, prefix="task")
			if task_form.is_valid():
				new_task = task_form.save(commit=False)
				new_task.project_id = project_id
				new_task.save()
				return HttpResponseRedirect(reverse('projects.views.project_single',args=[project_id]) + "#tasks")
		else:
			task_form = TaskAddForm(prefix="task")
			
		if 'edit_form' in request.POST:
			edit_form = ProjectAddForm(request.POST,instance=project,prefix="project")
			if edit_form.is_valid():
				edit_project = edit_form.save(commit=False)
				edit_project.company_id = project.company_id
				edit_project.save()
				return HttpResponseRedirect(reverse('projects.views.project_single',args=[project_id]) + "#overview")
		else:
			edit_form = ProjectAddForm(instance=project,prefix="project")

	else:
		document_form = DocumentAddForm(prefix="document")
		memo_form = MemoAddForm(prefix="memo")
		task_form = TaskAddForm(prefix="task")
		edit_form = ProjectAddForm(instance=project,prefix="project")

	return render(request,"project_single.html",{
		'project' : project,
		'documents' : documents,
		'memos' : memos,
		'tasks' : tasks,
		'edit_form' : edit_form,
		'memo_form' : memo_form,
		'document_form' : document_form,
		'task_form' : task_form,
	})

	
@login_required()
def document_delete(request,document_id):
	document = get_object_or_404(Document,id=document_id)
	project_id = document.project_id
	if user_can_access_project(request.user,project_id):
		document.file.delete()
		document.delete()
		return HttpResponseRedirect(reverse('project_single', args=[project_id]) + "#documents")
	else:
		return HttpResponse("You are not allowed to access this",status=403)

		
def document_single(request,document_id,key=""):
	document = get_object_or_404(Document,id=document_id)
	public_url = request.build_absolute_uri(reverse('document_public', args=[document.id,document.auth_key()]))
	
	if user_can_access_project(request.user,document.project_id) and key != document.auth_key():
		if request.POST:
			if 'email_form' in request.POST:
				email_form = DocumentEmailForm(request.POST,document=document,user=request.user,public_url=public_url,prefix="email")
				if email_form.is_valid():
					from django.core.mail import send_mail
					send_mail(document.title, email_form.cleaned_data['message'], email_form.cleaned_data['sender'], [email_form.cleaned_data['recipients']])
					return HttpResponseRedirect(reverse('projects.views.document_single',args=[document_id]))
			else:
				email_form = DocumentEmailForm(request.POST,document=document,user=request.user,public_url=public_url,prefix="email")
				
			if 'edit_form' in request.POST:
				edit_form = DocumentEditForm(request.POST,instance=document,prefix="document")
				if edit_form.is_valid():
					edit_document = edit_form.save(commit=False)
					edit_document.project_id = document.project_id
					edit_document.save()
					return HttpResponseRedirect(reverse('projects.views.document_single',args=[document_id]) + "#file")
			else:
				edit_form = DocumentEditForm(request.POST,instance=document,prefix="document")
		else:
			edit_form = DocumentEditForm(instance=document)
			email_form = DocumentEmailForm(document=document,user=request.user,public_url=public_url)
			
		return render(request,"document_single.html",{
			'document' : document,
			'public_url' : public_url,
			'edit_form' : edit_form,
			'email_form' : email_form,
			'is_public': False
		})
	elif key == document.auth_key():
		return render(request,"document_single.html",{
			'document' : document,
			'public_url' : public_url,
			'is_public': True
		})
	else:
		return HttpResponse("You are not allowed to access this",status=403)
	

@login_required()	
def memo_delete(request,memo_id):
	memo = get_object_or_404(Memo,id=memo_id)
	project_id = memo.project_id
	if user_can_access_project(request.user,project_id):
		memo.delete()
		return HttpResponseRedirect(reverse('project_single', args=[project_id]) + "#memos")
	else:
		return HttpResponse("You are not allowed to access this",status=403)
	
	
@login_required()
def project_delete(request,project_id):
	project = get_object_or_404(Project,id=project_id)
	if user_can_access_project(request.user,project.id):
		project.delete()
		return HttpResponseRedirect(reverse('home'))
	else:
		return HttpResponse("You are not allowed to access this",status=403)

		
@login_required()
def task_status(request,task_id,task_status):
	task = get_object_or_404(Task,id=task_id)
	task.status = task_status
	task.save()
	return HttpResponse(status=200)

	
@login_required
def memo_edit(request,memo_id): #Returns or processes an AJAX form
	memo = get_object_or_404(Memo,id=memo_id)
	if user_can_access_project(request.user,memo.project_id):
		if not request.POST:
			memo_form = MemoAddForm(instance=memo,prefix="memo")
			return render(request,"memo_edit.html",{
				'memo' : memo,
				'memo_form' : memo_form
			})
		if request.POST:
			memo_form = MemoAddForm(request.POST,instance=memo,prefix="memo")
			if memo_form.is_valid():
				edit_memo = memo_form.save(commit=False)
				edit_memo.project_id = memo.project_id
				edit_memo.save()
				return HttpResponseRedirect(reverse('project_single', args=[memo.project_id]) + "#memos")
		#The code below only runs if the form is not valid, or not yet submitted
		memo_form = MemoAddForm(instance=memo,prefix="memo")
		return render(request,"memo_edit.html",{
			'memo' : memo,
			'memo_form' : memo_form
		})
	else:
		return HttpResponse("You are not allowed to access this",status=403)#Forbidden

		
@login_required()
def task_list(request,project_id=None):
	company_id = request.user.get_profile().company.id
	if not project_id == None:
		tasks = Task.objects.filter(project = project_id).exclude(status = 0)
		project = get_object_or_404(Project,id=project_id)
	else:
		projects = Project.objects.filter(company_id = company_id).exclude(status = 0)
		tasks = Task.objects.filter(project__in = projects).exclude(status = 0)
		project = None
	return render(request,"task_list.html",{
		'tasks' : tasks,
		'project' : project
	})

	
@login_required()
def task_all(request,project_id=None):
	company_id = request.user.get_profile().company.id
	if not project_id == None:
		tasks = Task.objects.filter(project = project_id).exclude(status = 0)
		project = get_object_or_404(Project,id=project_id)
	else:
		projects = Project.objects.filter(company_id = company_id).exclude(status = 0)
		tasks = Task.objects.filter(project__in = projects).exclude(status = 0)
		project = None
	return render(request,"task_all.html",{
		'tasks' : tasks,
		'project' : project
	})

	
@login_required()
def project_status(request,project_id,project_status):
	project = get_object_or_404(Project,id=project_id)
	project.status = project_status
	project.save()
	return HttpResponse(status=200)
	

@login_required()
def comment_delete(request, message_id):
	comment = get_object_or_404(comments.get_model(), pk=message_id,site__pk=settings.SITE_ID)
	if comment.user == request.user or comment.user == None:
		comment.is_removed = True
		comment.save()
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=403)