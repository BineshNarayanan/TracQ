from django.conf.urls import patterns, url

from IssueTrackingSystem import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^login', views.login_user, name='login'),
	url(r'^logout', views.logout_user, name='logout'),
	url(r'^postIssue', views.postIssue, name='postIssue'),
	url(r'^postquery', views.postQueryPage, name='postQueryPage'),
	url(r'^home', views.goHome, name='home'),
	url(r'^openQueries', views.openQueries, name='openQueries'),
	url(r'^resolvedQueries', views.resolvedQueries, name='resolvedQueries'),
	url(r'^assignResolvers', views.assignIssuesToResolvers, name='assignQueries'),
	url(r'^editQuery', views.editQuery, name='editQuery'),
	url(r'^editIssue', views.editIssue, name='saveEditedIssue'),
	url(r'^viewquery', views.viewquery, name='viewQuery'),
)

'''
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	#url(r'^login', views.login, name='login'),
	#url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'IssueTrackingSystem/index.html'}),
	#url(r'^logout', views.logout, name='logout'),
	#url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^postIssue', views.postIssue, name='postIssue'),
	url(r'^postQueryPage', views.postQueryPage, name='postQueryPage'),
	url(r'^goHome', views.goHome, name='home'),
	url(r'^openQueries', views.openQueries, name='openQueries'),
	url(r'^resolvedQueries', views.resolvedQueries, name='resolvedQueries'),
	url(r'^assignResolvers', views.assignIssuesToResolvers, name='assignQueries'),
	url(r'^editQuery', views.editQuery, name='editQuery'),
	url(r'^editIssue', views.editIssue, name='saveEditedIssue'),
	url(r'^viewquery', views.viewquery, name='viewQuery'),
	#url(r'^login/$', views.login_user, name='login_user'),
)
'''