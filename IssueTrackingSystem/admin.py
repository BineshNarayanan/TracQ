from django import forms
from django.contrib import admin
from IssueTrackingSystem.models import Issue
from IssueTrackingSystem.models import Users
from IssueTrackingSystem.models import IssueTypeMaster
from IssueTrackingSystem.models import RoleMaster
from IssueTrackingSystem.models import IssueAssigneeHistory, IssueCommentLog, IssueAttachmentLog


# Register your models here.
admin.site.register(Issue)
admin.site.register(Users)
admin.site.register(IssueTypeMaster)
admin.site.register(RoleMaster)
admin.site.register(IssueAssigneeHistory)
admin.site.register(IssueCommentLog)
admin.site.register(IssueAttachmentLog)

class IssueForm(forms.ModelForm):
	class Meta:
		model = Issue

class IssueAdmin(admin.ModelAdmin):
    exclude = ['LastUpdateDate']
    form = IssueForm