from django.http import HttpResponse,Http404
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from time import time

from .models import OpenDataPortal
from .models import LoadRound
from .models import Tag
from .models import GlobalTag
from .models import GlobalGroup
from .models import Group
from .models import Dataset

from django.db.models import Q

def VocabularyRDFView(request):
	template = loader.get_template('tag_analytics/rdf/stodap.rdf')
	return HttpResponse(template.render(None,request), content_type = 'application/rdf+xml')

def SemanticTagRdfDetailView(request,pk):
	template = loader.get_template('tag_analytics/rdf/semantictag.rdf')
	context = { 'semantictag' : GlobalTag.objects.get(pk = pk),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def TagRdfDetailView(request,pk):
	template = loader.get_template('tag_analytics/rdf/tag.rdf')
	context = { 'tag' : Tag.objects.get(pk = pk),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def GroupRdfDetailView(request,pk):
	template = loader.get_template('tag_analytics/rdf/group.rdf')
	context = { 'group' : Group.objects.get(pk = pk),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def DatasetRdfDetailView(request,pk):
	template = loader.get_template('tag_analytics/rdf/dataset.rdf')
	context = { 'dataset' : Dataset.objects.get(pk = pk),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def SemanticGroupRdfDetailView(request,pk):
	template = loader.get_template('tag_analytics/rdf/semanticgroup.rdf')
	context = { 'semanticgroup' : GlobalGroup.objects.get(pk = pk),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def OpenDataPortalRdfDetailView(request,pk):
	template = loader.get_template('tag_analytics/rdf/opendataportal.rdf')
	context = { 'opendataportal' : OpenDataPortal.objects.get(pk = pk),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def SemanticTagRdfListView(request):
	template = loader.get_template('tag_analytics/rdf/semantictags.rdf')
	context = { 'semantictag_list' : GlobalTag.objects.all(),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def TagRdfListView(request,start=0,step=50):
	template = loader.get_template('tag_analytics/rdf/tags.rdf')
	end = int(start) + int(step)
	context = { 'tag_list' : Tag.objects.all()[start:end],
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def GroupRdfListView(request):
	template = loader.get_template('tag_analytics/rdf/groups.rdf')
	context = { 'group_list' : Group.objects.all(),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def DatasetRdfListView(request,start=0,step=50):
	template = loader.get_template('tag_analytics/rdf/datasets.rdf')
	end = int(start) + int(step)
	context = { 'dataset_list' : Dataset.objects.all()[start:end],
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def SemanticGroupRdfListView(request):
	template = loader.get_template('tag_analytics/rdf/semanticgroups.rdf')
	context = { 'semanticgroup_list' : GlobalGroup.objects.all(),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')

def OpenDataPortalRdfListView(request):
	template = loader.get_template('tag_analytics/rdf/opendataportals.rdf')
	context = { 'opendataportal_list' : OpenDataPortal.objects.all(),
				'vocab_host' : settings.VOCAB_HOST}
	return HttpResponse(template.render(context,request), content_type = 'application/rdf+xml')
