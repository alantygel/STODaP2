from django.http import HttpResponse,Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime

from .models import OpenDataPortal
from .models import LoadRound
from .models import Tag
from .models import GlobalTag
from .models import GlobalGroup
from .models import Group

import lib
import json
from functions import CalculateStats
from functions import CalculateCoocurrenceMatrix
from functions import LexicalCleaning
from functions import SyntacticSimilarity

from django.db.models import Q
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet


def autocomplete(request):
	sqs = SearchQuerySet().autocomplete(name_auto=request.GET.get('q', ''))[:5]
	suggestions = [result.object.name for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
	the_data = json.dumps({
        'results': suggestions
    })
	return HttpResponse(the_data, content_type='application/json')

class MySearchView(SearchView):
	"""My custom search view."""
	template_name = 'search/search.html'
	context_object_name = 'page_object'

	def get_queryset(self):
		queryset = super(MySearchView, self).get_queryset()
		# print queryset
        # further filter queryset based on some set of criteria
		return queryset

	def get_context_data(self, *args, **kwargs):
		context = super(MySearchView, self).get_context_data(*args, **kwargs)
		# print context
        # do something
		return context

class MySearchSpecView(SearchView):
	"""My custom search view."""
	template_name = 'search/search_specific.html'
	context_object_name = 'page_object'

	def get_queryset(self):
		queryset = super(MySearchSpecView, self).get_queryset()

        # further filter queryset based on some set of criteria
		return queryset

	def get_context_data(self, *args, **kwargs):
		context = super(MySearchSpecView, self).get_context_data(*args, **kwargs)
        # do something
		return context

class IndexView(generic.ListView):
    template_name = 'tag_analytics/index.html'
    context_object_name = 'groups_and_tags'

    def get_queryset(self):
		context = {
			'globalgroups' : GlobalGroup.objects.order_by('name')[:5],
			'globaltags' : GlobalTag.objects.order_by('name')[:5],
		}
		return context

class GlobalGroupIndexView(generic.ListView):
	model = GlobalGroup
	paginate_by = 30

	def get_queryset(self):
		return GlobalGroup.objects.order_by('name')

class GlobalTagIndexView(generic.ListView):
	model = GlobalTag
	paginate_by = 30

	def get_queryset(self):
		return GlobalTag.objects.order_by('name')

class ODPIndexView(generic.ListView):
	model = OpenDataPortal
	paginate_by = 30

	def get_queryset(self):
		return OpenDataPortal.objects.order_by('url')

class ODPDetailView(generic.DetailView):
    model = OpenDataPortal
    template_name = 'tag_analytics/opendataportal.html'

class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'tag_analytics/tag.html'

class GroupDetailView(generic.DetailView):
    model = Group
    template_name = 'tag_analytics/group.html'

class GlobalTagDetailView(generic.DetailView):
    model = GlobalTag
    template_name = 'tag_analytics/globaltag.html'

class GlobalGroupDetailView(generic.DetailView):
    model = GlobalGroup
    template_name = 'tag_analytics/globalgroup.html'

class DetailView(generic.DetailView):
    model = LoadRound
    template_name = 'tag_analytics/detail.html'


def edit_groups(request):
	for r in request.POST.getlist('global_group_group'):
		r = r.split('#')
		gg = GlobalGroup.objects.get(id = r[0])
		g = Group.objects.get(id = r[1])
		gg.groups.remove(g)
		
	groups = GlobalGroup.objects.all()
	context = {
		'global_groups' : groups
	}

	template = loader.get_template('tag_analytics/groups.html')
	return HttpResponse(template.render(context,request))

def global_tags(request):
	gt = GlobalTag.objects.all()
	context = {
		'global_tags' : gt
	}
	template = loader.get_template('tag_analytics/global_tags.html')
	return HttpResponse(template.render(context,request))

def show_tags(request):

	rounds = LoadRound.objects.filter(Q(id=70) | Q(id=2) | Q(id=11))
	all_tags = []
	for r in rounds:
		local_tags = r.tag_set.all()
		for tag in local_tags:
			if tag.main_tag == True:
				all_tags.append(tag)


#	round_tags = []
#	clean_local_tags = []
#	for r in rounds:
#		local_tags = r.tag_set.all()
#		for tag in local_tags:
#			if LexicalCleaning(tag):
#				clean_local_tags.append(tag)

#		round_tags.append(SyntacticSimilarity(clean_local_tags))
#	
#	tag_tras


	context = {
		'all_tags' : all_tags}

	template = loader.get_template('tag_analytics/show_tags.html')
	return HttpResponse(template.render(context, request))

def groups(request):
	groups = GlobalGroup.objects.all()
	template = loader.get_template('tag_analytics/groups.html')
	context = {
		'global_groups' : groups
	}
	return HttpResponse(template.render(context, request))

def show_statistics(request,roundn):

	rounds_success = LoadRound.objects.filter(roundn=roundn, success=1)
	rounds_failled = LoadRound.objects.filter(roundn=roundn, success=0)
	rounds_yellow = filter(lambda x: x.number_of_tags() > 0, rounds_failled)
	rounds_red = filter(lambda x: x.number_of_tags() == 0, rounds_failled)

	stats = CalculateStats(rounds_success)

	template = loader.get_template('tag_analytics/stats.html')
	context = {
		'round_number' : roundn,
		'odps_yellow' : len(rounds_yellow),
		'odps_red' : len(rounds_red),
		'number_of_odps': len(rounds_success),
		'stats': stats,
	}

	return HttpResponse(template.render(context, request))

def calculate_cooc_matrix(request):
	rounds = LoadRound.objects.filter(roundn=1, success=1)
	for r in rounds:
		CalculateCoocurrenceMatrix(r)
	return HttpResponse("bla")

def load_odps(request):
	"Reads the instance files, and initialize a list of ODP objects"

	with open("/home/alan/Dropbox/Alan - Doutorado/ODP_tag_analysis/django_project/tag_analytics/instances.json", 'r') as f:
		instances = json.loads(f.read())

	print 'Number of instances: ' + str(len(instances))

	for i in instances:
		if 'url-api' in i:
			odp_url = i['url-api']
		else:
			odp_url = i['url']
	
		o = OpenDataPortal(url=odp_url)
		o.save()

	return render (request,'tag_analytics/index.html')

def load_all(request,start=None):
	odps = OpenDataPortal.objects.all()

	if start:
		odps = odps[int(start):len(odps)]

	for o in odps:
		print o.url
		load_metadata(request,o.id,None)

	return render (request,'tag_analytics/index.html')

def load_metadata(request, open_data_portal_id,rnumber=None):

	try:
		o = OpenDataPortal.objects.get(id=open_data_portal_id)
	except:
		return
#		raise Http404("No ODP with id " + open_data_portal_id)
	## create round or laod
	if rnumber is not None:
		try:
			lr = o.loadround_set.get(roundn = rnumber)
		except:
			raise Http404("No round with this number: " + rnumber)
		lr.delete()
		lr = o.loadround_set.create(roundn = rnumber, success = 0)
	else:
		if o.loadround_set.count() > 0:
			rnumber = o.loadround_set.last().roundn + 1
		else:
			rnumber = 1
		lr = o.loadround_set.create(roundn = rnumber)

	## get tags
	tag_list_response = 0
	tag_list = 0
	try:		
		tag_list_response = lib.urlopen_with_retry(o.url + '/api/3/action/tag_list?all_fields=True')
	except:
		lr.success = 0
		lr.save()
		print "Website not available while getting tags"
		return
#		raise Http404("Website not available while getting tags")


	if tag_list_response: 
		try: 
			tag_list_dict = json.loads(tag_list_response.read())	
			tag_list = tag_list_dict['result']
		except:
			return
#			raise Http404("No results")

		print "adding tags"
		for tag in tag_list:
			lr.tag_set.create(name=tag.get('name'),display_name=tag.get('display_name'), ckan_id = tag.get('id'))

	## get groups
	group_list_response = 0
	group_list = 0
	try:		
		group_list_response = lib.urlopen_with_retry(o.url + '/api/3/action/group_list?all_fields=True')
	except:
		print "skipping groups"
		1 == 1
#		raise Http404("Website not available while getting groups")

	if group_list_response: 
		try: 
			group_list_dict = json.loads(group_list_response.read())	
			group_list = group_list_dict['result']
		except:
			print("No results")

		for group in group_list:
			lr.group_set.create(name=group.get('name'),display_name=group.get('display_name'), ckan_id = group.get('id'), 	n_packages = group.get('package_count'))


	print "getting datasets"
	## get datasets
	LIMIT = 50
	START = 0
	dataset_list_response = 0
	dataset_list = []
	keeploading = True

	print o.url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START)

	while keeploading:
		try:
			dataset_list_response = lib.urlopen_with_retry(o.url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START))
		except:
			lr.success = 0
			lr.save()
			print "Website not available while getting datasets"
			return
			raise Http404("Website not available while getting datasets")

		if dataset_list_response: 
			try: 
				dataset_list_dict = json.loads(dataset_list_response.read())	
#				dataset_list += dataset_list_dict['result']['results']
				dataset_list = dataset_list_dict['result']['results']
			except:
				print "No results"
	#			raise Http404("No results")
				return

			print o.url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START)
#			print len(dataset_list_dict['result']['results'])
			print dataset_list_dict['result']['count']
			print len(dataset_list)
			print lr.dataset_set.count()
			print "---"
#			if (len(dataset_list) >= int(dataset_list_dict['result']['count'])) or (START > dataset_list_dict['result']['count']):
			if (lr.dataset_set.count() >= int(dataset_list_dict['result']['count'])) or (len(dataset_list) == 0):
				keeploading = False
			else:
				START += LIMIT

			for dataset in dataset_list:
				if dataset.get('name') == "actuaciones-de-fiscalizacion":
					print "here"	
				dataset_response = 0
				if type(dataset['title']) is dict:
					dataset_name = dataset.get('title').values()[0]
				else:
					dataset_name = dataset.get('title')
		#		print "dataset name: " + dataset_name
				d = lr.dataset_set.create(name=dataset.get('name'),display_name=dataset_name, ckan_id = dataset.get('id'), metadata_modified = dataset.get('metadata_modified'), n_tags = dataset.get('num_tags'), n_resources = dataset.get('num_resources'))
				d.save()

				if type(dataset.get('tags')) is list:
					for tag in dataset.get('tags'):
						try:
							d.tag_set.add(lr.tag_set.get(ckan_id=tag.get('id')))
						except:
							print "error adding tag " + tag.get('name') + " to dataset " + dataset.get('name')
		#			print "---"

				if type(dataset.get('groups')) is list:
					for group in dataset.get('groups'):
		#				print ">> " + group.get('name')
						try:
							d.groups.add(lr.group_set.get(ckan_id=group.get('id')))
						except:
							print "error adding group " + group.get('name') + " to dataset " + dataset.get('name')
		#			print "---"


	## get metadata
	metadata_response = 0
	try:		
		metadata_response = lib.urlopen_with_retry(o.url + '/api/3/action/status_show?1=1')
	except:
		lr.success = 0
		lr.save()
		print "Website not available while getting metadata"
		return
#		raise Http404("Website not available while getting metadata")

	if metadata_response:
		try: 
			metadata_dict = json.loads(metadata_response.read())	
			metadata = metadata_dict['result']
		except:
			print "No results"
			return
#			raise Http404("No results")

		lr.odpmetadata_set.create(site_title = metadata['site_title'], ckan_version=metadata['ckan_version'], site_description=metadata['site_description'], locale_default=metadata['locale_default'], n_packages = dataset_list_dict['result']['count'])

	lr.success = 1
	lr.save()

	return HttpResponse("bla")

