from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^start/$', views.index, name='index'),
	url(r'^initialize/$', views.initialize, name='initialize'),
	url(r'^finish/$', views.finish, name='finish'),
	url(r'^entry_form/$', views.entry_form, name='entry_form'),
	url(r'^show_task/$', views.show_task, name='show_task'),

	url(r'^quest_answers/$', views.quest_answers, name='quest_answers'),
	url(r'^subject/(?P<pk>[0-9]+)/$', views.SubjectDetailView.as_view(), name='subject'),
	url(r'^subject/$', views.SubjectListView.as_view(), name='subject'),
	url(r'^subject_edit/$', views.subject_edit, name='subject_edit'),
	url(r'^correlations/$', views.correlations, name='correlations'),
]