from django.conf.urls import include, url
from django.conf.urls import *
from . import views
from . import views_rdf

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^vocabulary/$', views.VocabularyView.as_view(), name='vocabulary'),
    url(r'^semanticgroup/$', views.GlobalGroupIndexView.as_view(), name='globalgroup_list'),
    url(r'^semantictag/$', views.GlobalTagIndexView.as_view(), name='globaltag_list'),
    url(r'^dataset/$', views.DatasetIndexView.as_view(), name='dataset_list'),
    url(r'^semantictag/(?P<char>[a-z])/$', views.globaltag_list_alpha, name='globaltag_list_alpha'),
    url(r'^semanticgroup/(?P<char>[a-z])/$', views.globalgroup_list_alpha, name='globalgroup_list_alpha'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagDetailView.as_view(), name='tag'),
    url(r'^dataset/(?P<pk>[0-9]+)/$', views.DatasetDetailView.as_view(), name='dataset'),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(), name='group'),
    url(r'^semantictag/(?P<pk>[0-9]+)/$', views.GlobalTagDetailView.as_view(), name='globaltag'),
    url(r'^semanticgroup/(?P<pk>[0-9]+)/$', views.GlobalGroupDetailView.as_view(), name='globalgroup'),
	url(r'^search_specific/', views.MySearchSpecView.as_view(),name='search_specific'),
	url(r'^search/?$', views.MySearchView.as_view(), name='search'),
	url(r'^search/autocomplete/', views.autocomplete,name='autocomplete'),
    url(r'^opendataportals/$', views.ODPIndexView.as_view(), name='opendataportal_list'),
    url(r'^opendataportals_edit/$', views.ODPEditIndexView.as_view(), name='opendataportal_list_edit'),
    url(r'^opendataportal/(?P<pk>[0-9]+)/$', views.ODPDetailView.as_view(), name='opendataportal'),
    url(r'^load_metadata/(?P<open_data_portal_id>[0-9]+)$', views.load_metadata, name='load_metadata'),
    url(r'^process_round/(?P<round_id>[0-9]+)$', views.process_round, name='process_round'),

    url(r'^load_odps/$', views.load_odps, name='load_odps'),
    url(r'^edit_groups/$', views.edit_groups, name='edit_groups'),
    url(r'^calculate_cooc_matrix/$', views.calculate_cooc_matrix, name='calculate_cooc_matrix'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^show_stats/(?P<roundn>[0-9]+)/$', views.show_statistics, name='show_stats'),
    url(r'^show_tags/$', views.show_tags, name='show_tags'),
    url(r'^(?P<open_data_portal_id>[0-9]+)/load/(?P<rnumber>[0-9]+)$', views.load_metadata, name='load'),
    url(r'^(?P<open_data_portal_id>[0-9]+)/load/$', views.load_metadata, name='load'),
    url(r'^load_all/(?P<start>[0-9]+)$', views.load_all, name='load'),
    url(r'^faceted_search/$', views.FacetedSearchView.as_view(), name='faceted_search'),

    url(r'^semantictag/(?P<pk>[0-9]+).rdf$', views_rdf.SemanticTagRdfDetailView, name='semantictag_rdf'),
    url(r'^tag/(?P<pk>[0-9]+).rdf$', views_rdf.TagRdfDetailView, name='tag_rdf'),
    url(r'^group/(?P<pk>[0-9]+).rdf$', views_rdf.GroupRdfDetailView, name='group_rdf'),
    url(r'^dataset/(?P<pk>[0-9]+).rdf$', views_rdf.DatasetRdfDetailView, name='dataset_rdf'),
    url(r'^semanticgroup/(?P<pk>[0-9]+).rdf$', views_rdf.SemanticGroupRdfDetailView, name='semanticgroup_rdf'),
    url(r'^opendataportal/(?P<pk>[0-9]+).rdf$', views_rdf.OpenDataPortalRdfDetailView, name='opendataportal_rdf'),

    url(r'^vocabulary.rdf$', views_rdf.VocabularyRDFView, name='vocabulary_rdf'),
    url(r'^semantictag.rdf$', views_rdf.SemanticTagRdfListView, name='semantictags_rdf'),
    url(r'^tag/(?P<start>[0-9]+)/(?P<step>[0-9]+)/rdf$', views_rdf.TagRdfListView, name='tags_rdf'),
    url(r'^group.rdf$', views_rdf.GroupRdfListView, name='groups_rdf'),
    url(r'^dataset/(?P<start>[0-9]+)/(?P<step>[0-9]+)/rdf$', views_rdf.DatasetRdfListView, name='datasets_rdf'),
    url(r'^semanticgroup.rdf$', views_rdf.SemanticGroupRdfListView, name='semanticgroups_rdf'),
    # url(r'^opendataportal.rdf$', views_rdf.OpenDataPortalRdfListView, name='opendataportals_rdf'),

    url(r'^opendataportal.rdf$', views_rdf.PrintOpenDataPortalRdfListView, name='opendataportals_rdf'),
    url(r'^tag.rdf$', views_rdf.PrintTagRdfListView, name='tags_rdf'),
    url(r'^dataset.rdf$', views_rdf.PrintDatasetRdfListView, name='datasets_rdf'),

]

    



