from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from IssueTrackingSystem.models import Issue, Users, IssueTypeMaster, RoleMaster, IssueAssigneeHistory, IssueCommentLog, IssueAttachmentLog
from IssueTracker.settings import FILESAVE_PATH

import datetime
#import smtplib


'''
def index(request):
	return HttpResponse("Hello, Welcome to the IssueTrackingSystem.")
'''

def index(request):
	template = loader.get_template('IssueTrackingSystem/index.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def logout_user(request):
	logout(request)
	template = loader.get_template('IssueTrackingSystem/index.html')
	context = RequestContext(request, {})
	#return HttpResponse(template.render(context))
	return HttpResponseRedirect('/IssueTrackingSystem')

def validateSession(request):
	if request.session:
		return True
	return False

def login_user(request):
	username = request.POST.get('txtUserId');
	password = request.POST.get('txtPassword');
	user = authenticate(username=username, password=password)
	if user is not None:
		# the password verified for the user
		if user.is_active:
			print("User is valid, active and authenticated")
			login(request, user)
			loggedInUser = Users.objects.get(LoginId=user.username)
			request.session['LOGGED_IN_USER_ROLE'] = loggedInUser.RoleMasterCode.RoleMasterCode
			request.session['LOGGED_IN_USER_ID'] = loggedInUser.Id
			if loggedInUser.RoleMasterCode.RoleMasterCode == 'ADM':
				return HttpResponseRedirect('/IssueTrackingSystem/dashboard')
			else:
				return HttpResponseRedirect('/IssueTrackingSystem/dashboard')
		else:
			print("The password is valid, but the account has been disabled!")
			return index(request)
	else:
		# the authentication system was unable to verify the username and password
		print("The username and password were incorrect.")
	return index(request)

'''	
def login(request):
	context = RequestContext(request, {})
	isUserAuthenticated = False;
	if request.method == 'GET':
		name = request.GET.get('txtEmail');
		listIssues = Issue.objects.filter(IssueAssignedTo=0)
		listAdminUsers = Users.objects.filter(RoleMasterCode='ADM')
		context = RequestContext(request, {
			'listIssues': listIssues,
			'listAdminUsers' : listAdminUsers,
		})
		return HttpResponse(template.render(context))
		#return HttpResponse("You have logged in successfully as "+ name +" through GET..")
	elif request.method == 'POST':
		emailId = request.POST.get('txtEmail');
		try:
			user = Users.objects.get(EmailId=emailId)
			if user:
				if user.Password == request.POST.get('txtPassword'):
					isUserAuthenticated = True
					template = loader.get_template('IssueTrackingSystem/home.html')
					listIssues = Issue.objects.all()
					listAdminUsers = Users.objects.filter(RoleMasterCode='ADM')
					request.session['FirstName'] = user.FirstName
					request.session['LastName'] = user.LastName
					context = RequestContext(request, {
						'listIssues': listIssues,
						'listAdminUsers' : listAdminUsers,
					})
					return HttpResponse(template.render(context))
				else:
					errorMessage =	'Incorrect Password!!'
		except:
			errorMessage = 'User does not exist!!'
	template = loader.get_template('IssueTrackingSystem/index.html')
	context = RequestContext(request, {'isUserAuthenticated': isUserAuthenticated,'errorMessage' : errorMessage})
	return HttpResponse(template.render(context))
'''

@login_required(login_url='/IssueTrackingSystem')
def goHome(request):
	template = loader.get_template('IssueTrackingSystem/home.html')
	LOGGED_IN_USER_ROLE = request.session['LOGGED_IN_USER_ROLE']
	listAdminUsers = []
	listResolvers = []
	listIssues = []
	if LOGGED_IN_USER_ROLE == 'ADM':
		unAssignedUser = Users.objects.get(RoleMasterCode='UA')
		listIssues = Issue.objects.filter(IssueAssignedTo=unAssignedUser,IsIssueOpen=True)
		listAdminUsers = list(Users.objects.filter(RoleMasterCode='ADM'))
		listResolvers = list(Users.objects.filter(RoleMasterCode='RES'))
		'''
		elif LOGGED_IN_USER_ROLE == 'RES':
			unAssignedUser = Users.objects.get(LoginId=request.user.username)
			listIssues = Issue.objects.filter(IssueAssignedTo=unAssignedUser,IsIssueOpen=True)
			listResolvers = list(Users.objects.filter(RoleMasterCode='RES'))
		else:
			#get issues posted by the user
			createdBy = Users.objects.get(LoginId=request.user.username)
			print createdBy
			print createdBy.Id
			listIssues = Issue.objects.filter(UserId=createdBy,IsIssueOpen=True)
			print listIssues
		'''
	context = RequestContext(request, {
		'listIssues': listIssues,
		'listAdminUsers' : listAdminUsers + listResolvers,
	})
	return HttpResponse(template.render(context))

@login_required(login_url='/IssueTrackingSystem')
def resolvedQueries(request):
	template = loader.get_template('IssueTrackingSystem/resolvedQueries.html')
	#listIssues = Issue.objects.filter(IssueAssignedTo__gt=0,IsIssueOpen=False)
	LOGGED_IN_USER_ROLE = request.session['LOGGED_IN_USER_ROLE']
	loggedInUser = Users.objects.get(LoginId=request.user.username)
	listIssues = []
	listIssuesPostedBySelf = []
	if LOGGED_IN_USER_ROLE == 'ADM':
		listIssues = Issue.objects.filter(IsIssueOpen=False)
		listIssuesPostedBySelf = Issue.objects.filter(IsIssueOpen=False,UserId=loggedInUser)
	elif LOGGED_IN_USER_ROLE == 'RES':
		listIssues = Issue.objects.filter(IsIssueOpen=False,IssueResolvedBy=loggedInUser)
		listIssuesPostedBySelf = Issue.objects.filter(IsIssueOpen=False,UserId=loggedInUser)
	else:
		listIssues = Issue.objects.filter(IsIssueOpen=False,UserId=loggedInUser)
	context = RequestContext(request, {
        'listIssues': listIssues,
		'listIssuesPostedBySelf':listIssuesPostedBySelf,
    })
	return HttpResponse(template.render(context))
	

@login_required(login_url='/IssueTrackingSystem')	
def openQueries(request):
	template = loader.get_template('IssueTrackingSystem/openQueries.html')
	LOGGED_IN_USER_ROLE = request.session['LOGGED_IN_USER_ROLE']
	loggedInUser = Users.objects.get(LoginId=request.user.username)
	listIssues = []
	listIssuesPostedBySelf = []
	if LOGGED_IN_USER_ROLE == 'ADM':
		unAssignedUser = Users.objects.get(RoleMasterCode='UA')
		listIssues = Issue.objects.filter(IsIssueOpen=True).exclude(IssueAssignedTo=unAssignedUser)
		listIssuesPostedBySelf = Issue.objects.filter(IsIssueOpen=True,UserId=loggedInUser)
	elif LOGGED_IN_USER_ROLE == 'RES':
		listIssues = Issue.objects.filter(IsIssueOpen=True,IssueAssignedTo=loggedInUser)
		listIssuesPostedBySelf = Issue.objects.filter(IsIssueOpen=True,UserId=loggedInUser)
	else:
		listIssues = Issue.objects.filter(IsIssueOpen=True,UserId=loggedInUser)
	#loggedInUser = Users.objects.get(Id=1)
	#listIssues = Issue.objects.filter(IssueAssignedTo=loggedInUser,IsIssueOpen=True)
	#listIssues = Issue.objects.select_related('Users').filter(IssueAssignedTo__gt=0)
	context = RequestContext(request, {
        'listIssues': listIssues,
		'listIssuesPostedBySelf':listIssuesPostedBySelf,
    })
	return HttpResponse(template.render(context))


@login_required(login_url='/IssueTrackingSystem')	
def postQueryPage(request):
	template = loader.get_template('IssueTrackingSystem/postquery.html')
	issueTypes = IssueTypeMaster.objects.all()
	context = RequestContext(request, {
		'issueTypes': issueTypes,
		'issueDate' : datetime.datetime.now(),
	})
	return HttpResponse(template.render(context))
	
def postIssue(request):
	template = loader.get_template('IssueTrackingSystem/openQueries.html')
	issueTitle = request.POST.get('txtIssueTitle');
	issueDescription = request.POST.get('txtIssueDescription');
	issueType = request.POST.get('txtIssueType');
	#loggedInUser = Users.objects.get(Id=1)
	loggedInUser = Users.objects.get(LoginId=request.user.username)
	userAssignedTo = Users.objects.get(RoleMasterCode='UA')
	issueTypeMaster = IssueTypeMaster.objects.get(IssueTypeCode=issueType)
	with transaction.atomic():
		issue = Issue(IssueTitle=issueTitle,IssueDescription=issueDescription,IssueTypeCode=issueTypeMaster,UserId=loggedInUser,IssueAssignedTo=userAssignedTo);
		issue.save();
		issueAssigneeHistory = IssueAssigneeHistory(IssueId=issue,IssueAssignedTo=userAssignedTo,IssueAssignedBy=loggedInUser,IssueAssignedOn=datetime.datetime.now())
		issueAssigneeHistory.save()
		if request.POST.get('file') != '':
			uploadedFile = request.FILES['file']
			fileName = uploadedFile.name
			issueId = issue.Id
			timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
			finalFileNameSaved = timestamp + '_' + str(issueId) + '_' + fileName
			issueAttachmentLog = IssueAttachmentLog(IssueId=issue,AttachmentName=fileName,AttachmentLocation=finalFileNameSaved,UploadedOn=datetime.datetime.now(),UploadedBy=loggedInUser)
			issueAttachmentLog.save()
			saveFile(request,finalFileNameSaved)
		sendemail(issue)
	return openQueries(request)



def assignIssuesToResolvers(request):
	#template = loader.get_template('IssueTrackingSystem/home.html')
	#listIssues = Issue.objects.all()
	selectedIssuesWithResolvers = request.GET.get('selectedIssues');
	print selectedIssuesWithResolvers
	listOfIssueIdWithResolvers = selectedIssuesWithResolvers.split(",",1)
	loggedInUser = Users.objects.get(Id=1)
	#print listOfIssueIdWithResolvers
	for issueIdWithResolver in listOfIssueIdWithResolvers:
		print issueIdWithResolver
		details = issueIdWithResolver.split(":",1)
		issueId = details[0]
		assignee = Users.objects.get(Id=details[1])
		with transaction.atomic():
			issue = Issue.objects.get(Id=issueId)
			issue.IssueAssignedTo = assignee
			issue.IssueAssignedOn = datetime.datetime.now()
			issue.save();
			issueAssigneeHistory = IssueAssigneeHistory(IssueId=issue,IssueAssignedTo=assignee,IssueAssignedBy=loggedInUser,IssueAssignedOn=datetime.datetime.now())
			issueAssigneeHistory.save()
	return goHome(request)

@login_required(login_url='/IssueTrackingSystem')
def editQuery(request):
	template = loader.get_template('IssueTrackingSystem/editquery.html')
	issueId = request.GET.get('issueId')
	issueTypes = IssueTypeMaster.objects.all()
	issue = Issue.objects.get(Id=issueId)
	listAdminUsers = list(Users.objects.filter(RoleMasterCode='ADM'))
	listResolvers = list(Users.objects.filter(RoleMasterCode='RES'))
	commentHistory = IssueCommentLog.objects.filter(IssueId=issue)
	issueAttachmentLog = IssueAttachmentLog.objects.filter(IssueId=issue)
	context = RequestContext(request, {
		'issue':issue,
		'issueTypes': issueTypes,
		'listAdminUsers':listAdminUsers + listResolvers,
		'commentHistoryLength' : len(commentHistory),
		'commentHistory':enumerate(commentHistory,start=1),
		'issueAttachmentLogLength':len(issueAttachmentLog),
		'issueAttachmentLog':enumerate(issueAttachmentLog,start=1)
	})
	return HttpResponse(template.render(context))

@login_required(login_url='/IssueTrackingSystem')
def editIssue(request):
	#template = loader.get_template('IssueTrackingSystem/openqueries.html')
	issueId = request.POST.get('issueId')
	assignTo = request.POST.get('assignTo')
	resolveQuery = request.POST.get('resolveQuery')
	comment = request.POST.get('nameTxtComment')
	issue = Issue.objects.get(Id=issueId)
	if resolveQuery == 'on':
		issue.IsIssueOpen = False
	loggedInUser = Users.objects.get(LoginId=request.user.username)
	#issue.IssueAssignedTo = issue.UserId
	issue.IssueAssignedTo = Users.objects.get(Id=assignTo)
	issue.IssueAssignedOn = datetime.datetime.now()
	issue.LastUpdateDate = datetime.datetime.now()
	issue.IssueResolvedBy = loggedInUser
	with transaction.atomic():
		issue.save()
		issueAssigneeHistory = IssueAssigneeHistory(IssueId=issue,IssueAssignedTo=issue.IssueAssignedTo,IssueAssignedBy=loggedInUser,IssueAssignedOn=datetime.datetime.now())
		issueAssigneeHistory.save()
		comments = IssueCommentLog(IssueId=issue,Comment=comment,CommentBy=loggedInUser,CommentedOn=datetime.datetime.now())
		comments.save()
		if request.POST.get('file') != '':
			uploadedFile = request.FILES['file']
			fileName = uploadedFile.name
			issueId = issue.Id
			timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
			finalFileNameSaved = timestamp + '_' + str(issueId) + '_' + fileName
			issueAttachmentLog = IssueAttachmentLog(IssueId=issue,AttachmentName=fileName,AttachmentLocation=finalFileNameSaved,UploadedOn=datetime.datetime.now(),UploadedBy=loggedInUser)
			issueAttachmentLog.save()
			saveFile(request,finalFileNameSaved)
	#listIssues = Issue.objects.filter(IssueAssignedTo__gt=0)
	#context = RequestContext(request, {
	#	'listIssues': listIssues
	#})
	return openQueries(request)

@login_required(login_url='/IssueTrackingSystem')
def viewquery(request):
	template = loader.get_template('IssueTrackingSystem/viewquery.html')
	issueId = request.GET.get('issueId')
	issue = Issue.objects.get(Id=issueId)
	issueTypes = IssueTypeMaster.objects.all()
	commentHistory = IssueCommentLog.objects.filter(IssueId=issue)
	issueAttachmentLog = IssueAttachmentLog.objects.filter(IssueId=issue)
	print commentHistory
	context = RequestContext(request, {
		'issue': issue,
		'issueTypes': issueTypes,
		'commentHistoryLength' : len(commentHistory),
		'commentHistory':enumerate(commentHistory,start=1),
		'issueAttachmentLogLength':len(issueAttachmentLog),
		'issueAttachmentLog':enumerate(issueAttachmentLog,start=1)
	})
	return HttpResponse(template.render(context))
	
def sendemail(issue):
	subject = "Acknowledgement for Query No. " + str(issue)
	message = "Hello,\n\nThanks for your mail.\n\nWe will revert to you within 48 hours.\n\nRegards,\nHR Team."
	disclaimer = "\n\nDISCLAIMER : This is an auto-generated mail. Please do not reply to this mail."
				
	send_mail(subject, message+disclaimer, 'HRTeam@morningstar.com',['binesh.narayanan@morningstar.com','swati.shettigar@morningstar.com'], fail_silently=False)

def viewDashboard(request):
	template = loader.get_template('IssueTrackingSystem/dashboard.html')
	LOGGED_IN_USER_ROLE = request.session['LOGGED_IN_USER_ROLE']
	loggedInUser = Users.objects.get(LoginId=request.user.username)
	unAssignedUser = Users.objects.get(RoleMasterCode='UA')
	listOpenIssues = []
	listUnassignedIssues = []
	listResolvedIssues = []
	if LOGGED_IN_USER_ROLE == 'ADM':
		listUnassignedIssues = Issue.objects.filter(IssueAssignedTo=unAssignedUser,IsIssueOpen=True)
		listResolvedIssues = Issue.objects.filter(IsIssueOpen=False)
		listOpenIssues = Issue.objects.filter(IsIssueOpen=True)
	elif LOGGED_IN_USER_ROLE == 'RES':
		listUnassignedIssues = Issue.objects.filter(IssueAssignedTo=unAssignedUser,IsIssueOpen=True)
		listResolvedIssues = Issue.objects.filter(IsIssueOpen=False,IssueResolvedBy=loggedInUser)
		listOpenIssues = Issue.objects.filter(IssueAssignedTo=loggedInUser,IsIssueOpen=True)
	else:
		listResolvedIssues = Issue.objects.filter(UserId=loggedInUser,IsIssueOpen=False)
		listOpenIssues = Issue.objects.filter(UserId=loggedInUser,IsIssueOpen=True)
	context = RequestContext(request, {
        'listOpenIssues': len(listOpenIssues),
		'listUnassignedIssues':len(listUnassignedIssues),
		'listResolvedIssues':len(listResolvedIssues),
    })
	return HttpResponse(template.render(context))

	
def postFile(request):
	template = loader.get_template('IssueTrackingSystem/postfile.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def saveFile(request,finalFileNameSaved):
	template = loader.get_template('IssueTrackingSystem/postfile.html')
	uploadedFile = request.FILES['file']
	with open(FILESAVE_PATH+finalFileNameSaved, 'wb+') as destination:
		for chunk in uploadedFile.chunks():
			destination.write(chunk)
	context = RequestContext(request, {})
	return postFile(request)