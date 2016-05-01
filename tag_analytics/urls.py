from django.conf.urls import include, url
from django.conf.urls import *
from haystack.forms import FacetedSearchForm
from haystack.generic_views import FacetedSearchView

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^globalgroups/$', views.GlobalGroupIndexView.as_view(), name='globalgroup_list'),
    url(r'^globaltags/$', views.GlobalTagIndexView.as_view(), name='globaltag_list'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagDetailView.as_view(), name='tag'),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(), name='group'),
    url(r'^globaltag/(?P<pk>[0-9]+)/$', views.GlobalTagDetailView.as_view(), name='globaltag'),
    url(r'^globalgroup/(?P<pk>[0-9]+)/$', views.GlobalGroupDetailView.as_view(), name='globalgroup'),
	url(r'^search_specific/', views.MySearchSpecView.as_view(),name='search_specific'),
	url(r'^search/?$', views.MySearchView.as_view(), name='search'),
	url(r'^search/autocomplete/', views.autocomplete,name='autocomplete'),
    url(r'^opendataportals/$', views.ODPIndexView.as_view(), name='opendataportal_list'),
    url(r'^opendataportal/(?P<pk>[0-9]+)/$', views.ODPDetailView.as_view(), name='opendataportal'),
    url(r'^load_odps/$', views.load_odps, name='load_odps'),
    url(r'^edit_groups/$', views.edit_groups, name='edit_groups'),
    url(r'^calculate_cooc_matrix/$', views.calculate_cooc_matrix, name='calculate_cooc_matrix'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^show_stats/(?P<roundn>[0-9]+)/$', views.show_statistics, name='show_stats'),
    url(r'^show_tags/$', views.show_tags, name='show_tags'),
    url(r'^(?P<open_data_portal_id>[0-9]+)/load/(?P<rnumber>[0-9]+)$', views.load_metadata, name='load'),
    url(r'^(?P<open_data_portal_id>[0-9]+)/load/$', views.load_metadata, name='load'),
    url(r'^load_all/(?P<start>[0-9]+)$', views.load_all, name='load'),
    url(r'^faceted_search/$', FacetedSearchView.as_view(context_object_name = 'page_object',template_name='search/faceted_search.html',form_class=FacetedSearchForm, facet_fields=['language','globaltags','portal']), name='faceted_search'),
]

    


