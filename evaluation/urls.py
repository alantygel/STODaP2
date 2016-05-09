from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^start/$', views.index, name='index'),
	url(r'^initialize/$', views.initialize, name='initialize'),
	url(r'^finish/$', views.finish, name='finish'),
	url(r'^entry_form/$', views.entry_form, name='entry_form'),
	url(r'^show_task/$', views.show_task, name='show_task'),
]