import datetime
from haystack import indexes
from tag_analytics.models import Tag
from tag_analytics.models import Dataset
from tag_analytics.models import GlobalTag
from tag_analytics.models import GlobalGroup

class TagIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	name = indexes.CharField(model_attr='display_name')
	insert_date = indexes.DateTimeField(model_attr='insert_date')

	def get_model(self):
		return Tag

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(insert_date__lte=datetime.datetime.now())

class DatasetIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	# name = indexes.CharField(model_attr='display_name')
	language = indexes.CharField(model_attr='get_language',faceted=True)
	portal = indexes.CharField(model_attr='get_portal',faceted=True)
	globaltags = indexes.MultiValueField(model_attr='get_globaltags',faceted=True)
	globalgroups = indexes.MultiValueField(model_attr='get_globalgroups',faceted=True)
	insert_date = indexes.DateTimeField(model_attr='insert_date')

	def get_model(self):
		return Dataset

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(insert_date__lte=datetime.datetime.now())

class GlobalTagIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
#	tags = indexes.MultiValueField(faceted=True)
	description = indexes.CharField(model_attr='name')
	insert_date = indexes.DateTimeField(model_attr='insert_date')

	name_auto = indexes.EdgeNgramField(model_attr='name')

	def get_model(self): 
		return GlobalTag

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(insert_date__lte=datetime.datetime.now())

	def prepare(self, obj):
		data = super(GlobalTagIndex, self).prepare(obj)
		data['boost'] = 5.0
		return data

# #	def prepare_tags(self, obj):
# #		return [t for t in obj.tags.all()]

class GlobalGroupIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	name = indexes.CharField(model_attr='name')
	insert_date = indexes.DateTimeField(model_attr='insert_date')

	def get_model(self):
		return GlobalGroup

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(insert_date__lte=datetime.datetime.now())

	def prepare(self, obj):
		data = super(GlobalGroupIndex, self).prepare(obj)
		data['boost'] = 5.0
		return data

