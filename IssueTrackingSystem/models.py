import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

'''
CREATE TABLE IssueTypeMaster (
  IssueTypeCode VARCHAR(3) NULL,
  IssueTypeDescription VARCHAR(30) NULL,
  IssuePriority INTEGER UNSIGNED NULL,
  PRIMARY KEY(Id)
);
'''

class IssueTypeMaster(models.Model):
	IssueTypeCode = models.CharField(primary_key=True,max_length=3)
	IssueTypeName = models.CharField(max_length=15)
	IssueTypeDescription = models.CharField(max_length=300)
	IssueTypePriority = models.PositiveIntegerField();
	def __unicode__(self):
		return unicode(self.IssueTypeCode)

'''
CREATE TABLE RoleMaster (
  RoleMasterCode VARCHAR(3) NULL,
  RoleName VARCHAR(50) NULL,
  RolePriority INTEGER UNSIGNED NULL,
  PRIMARY KEY(Id)
);
'''

class RoleMaster(models.Model):
	RoleMasterCode = models.CharField(primary_key=True,max_length=3)
	RoleName = models.CharField(max_length=15)
	RoleDescription = models.CharField(max_length=300)
	RolePriority = models.PositiveIntegerField();
	def __unicode__(self):
		return unicode(self.RoleName)

'''
CREATE TABLE Users (
  Id REAL NOT NULL AUTO_INCREMENT,
  FirstName VARCHAR(40) NULL,
  LastName VARCHAR(40) NULL,
  EmailId VARCHAR(50) NULL,
  LoginId VARCHAR(20) NULL,
  RoleMasterCode VARCHAR(3) NULL,
  PRIMARY KEY(Id)
);
'''

class Users(models.Model):
	Id = models.AutoField(primary_key=True)
	FirstName = models.CharField(max_length=100)
	LastName = models.CharField(max_length=100)
	EmailId = models.EmailField(max_length=250)
	LoginId = models.CharField(max_length=100)
	Password = models.CharField(max_length=100)
	RoleMasterCode = models.ForeignKey(RoleMaster)
	def __unicode__(self):
		return self.FirstName + ' ' +  self.LastName

'''
CREATE TABLE Issue (
  Id REAL NOT NULL AUTO_INCREMENT,
  Users_Id REAL NOT NULL,
  IssueTitle VARCHAR(200) NULL,
  IssueDescription VARCHAR(4000) NULL,
  IssueRaisedOn DATETIME NULL,
  IsIssueOpen BIT NULL,
  IsIssueReopened BIT NULL,
  LastUpdateDate DATETIME NULL,
  IssueTypeCode VARCHAR(3) NULL,
  PRIMARY KEY(Id),
  INDEX Issue_FKIndex1(Users_Id)
);
'''
class Issue(models.Model):
	Id = models.AutoField(primary_key=True)
	IssueTitle = models.CharField(max_length=500)
	IssueDescription = models.TextField(max_length=2000)
	#IssueRaisedOn = models.DateTimeField(default=datetime.datetime.now)timezone
	IssueRaisedOn = models.DateTimeField(default=timezone.now)
	IsIssueOpen = models.BooleanField(default=True)
	IsIssueReopened = models.BooleanField(default=False)
	LastUpdateDate = models.DateTimeField('Last Updated Date',default=datetime.datetime.now(),blank=True)
	IssueTypeCode = models.ForeignKey(IssueTypeMaster)
	UserId = models.ForeignKey(Users,related_name='Creator')
	IssueAssignedTo = models.ForeignKey(Users,related_name='Resolver')
	IssueAssignedOn = models.DateTimeField('Issue Assigned On',default=datetime.datetime.now(),blank=True)
	IssueResolvedBy = models.ForeignKey(Users,related_name='ResolvedBy')
	def __unicode__(self):
		return unicode(self.Id)
	
	
'''
CREATE TABLE IssueAssigneeHistory (
  Id REAL NOT NULL AUTO_INCREMENT,
  IssueId REAL NOT NULL,
  AssignedTo INT NULL,
  AssignedBy INT NULL,
  AssignedOn DATETIME NULL,
  PRIMARY KEY(Id)
);
'''

class IssueAssigneeHistory(models.Model):
	Id = models.AutoField(primary_key=True)
	IssueId = models.ForeignKey(Issue,related_name='Issue')
	IssueAssignedTo = models.ForeignKey(Users,related_name='IssueAssigneeHistory_Resolver')
	IssueAssignedBy = models.ForeignKey(Users,related_name='IssueAssigneeHistory_Assigner')
	IssueAssignedOn = models.DateTimeField('Issue Assigned On',default=datetime.datetime.now(),blank=True)
	def __unicode__(self):
		return unicode(self.Id)



'''
CREATE TABLE IssueCommentLog (
  Id REAL NOT NULL AUTO_INCREMENT,
  Issue_Id REAL NOT NULL,
  IssueComment VARCHAR(200) NULL,
  CommentBy INTEGER UNSIGNED NULL,
  CommentedOn DATETIME NULL,
  PRIMARY KEY(Id),
  INDEX IssueCommentLog_FKIndex1(Issue_Id)
);
'''

class IssueCommentLog(models.Model):
	Id = models.AutoField(primary_key=True)
	IssueId = models.ForeignKey(Issue,related_name='IssueComments')
	Comment = models.TextField(max_length=2000)
	CommentBy = models.ForeignKey(Users,related_name='CommentsByAssignee')
	CommentedOn = models.DateTimeField('Issue Assigned On',default=datetime.datetime.now(),blank=True)
	def __unicode__(self):
		return unicode(self.Id)