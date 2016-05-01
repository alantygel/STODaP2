from __future__ import unicode_literals
from datetime import datetime
from django.db import models
import numpy

class OpenDataPortal(models.Model):
	url = models.CharField(max_length=200)
	insert_date = models.DateTimeField('insert date', default=datetime.now)

	def __str__(self):
		return self.url

class LoadRound(models.Model):
	open_data_portal = models.ForeignKey(OpenDataPortal, on_delete=models.CASCADE)
	roundn = models.IntegerField(null=False,blank=False)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	success = models.IntegerField(default=0, null=False,blank=False)

	def __str__(self):
		return self.open_data_portal.url + '-' + str(self.roundn)

	def tags_per_dataset(self):
		r = numpy.array(map(lambda z: z.tag_set.count(), self.dataset_set.all()))
		return r.mean(), r.std()

	def datasets_per_group(self):
		r = numpy.array(map(lambda z: z.dataset_set.count(), self.group_set.all()))
		return r.mean(), r.std()

	def number_of_tags(self):
		return self.tag_set.count()

	def number_of_datasets(self):
		return self.dataset_set.count()


class ODPMetadata(models.Model):
	site_title = models.CharField(max_length=200, null=True,blank=True)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	ckan_version = models.CharField(max_length=200, null=True,blank=True)
	site_description = models.CharField(max_length=2000, null=True,blank=True)
	locale_default = models.CharField(max_length=10, null=True, blank=True)
	load_round = models.ForeignKey(LoadRound, on_delete=models.CASCADE)
	n_packages = models.IntegerField(default=0, null=True,blank=True)
	

	def __str__(self):
		return self.load_round.open_data_portal.url

class Group(models.Model):
	name = models.CharField(max_length=200)
	display_name = models.CharField(max_length=200,null=True,blank=True)
	ckan_id = models.CharField(max_length=200)
	load_round = models.ForeignKey(LoadRound, on_delete=models.CASCADE)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	n_packages = models.IntegerField(default=0, null=True,blank=True)
	translation = models.CharField(max_length=200,null=True,blank=True)

	def __unicode__(self):
		return self.translation if self.translation != None else self.display_name

	def translated(self):
		return self.translation if self.translation != None else self.display_name

	def get_tags(self):
		tags = []
		for d in self.dataset_set.all():
			for t in d.tag_set.all():
				tags.append(t)
		return set(tags)

class GlobalGroup(models.Model):
	name = models.CharField(max_length=200)
	groups = models.ManyToManyField(Group, blank=True)
	uri = models.CharField(max_length=400, blank=True)
	insert_date = models.DateTimeField('insert date', default=datetime.now)

	def __unicode__(self):
		return self.name

	def dataset_count(self):
		datasets = []
		for g in self.groups.all():
			datasets += g.dataset_set.all()
		for gt in self.globaltag_set.all():
			datasets += gt.datasets()
		return len(set(datasets))


class Dataset(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000,null=True,blank=True)
	display_name = models.CharField(max_length=200,null=True,blank=True)
	ckan_id = models.CharField(max_length=200)
	load_round = models.ForeignKey(LoadRound, on_delete=models.CASCADE)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	metadata_modified = models.DateTimeField('metadata_modified',default=None,null=True,blank=True)
	groups = models.ManyToManyField(Group, blank=True)
	n_tags = models.IntegerField(null=True,blank=True)
	n_resources = models.IntegerField(null=True,blank=True)

	def __unicode__(self):
		return self.name

	def get_language(self):
		try:
			return self.load_round.odpmetadata_set.first().locale_default
		except:
			return None

	def get_portal(self):
		return self.load_round.open_data_portal.url

	def get_url(self):
		url = self.load_round.open_data_portal.url + "/dataset/" + self.name
		if self.load_round.open_data_portal.url == "http://publicdata.eu":
			url += ".html" 
		return url

	def get_globaltags(self):
		globaltags = []
		tags = self.tag_set.all()
		for t in tags:
			for gt in t.globaltag_set.all():
				globaltags.append(gt)
		return globaltags

	def get_globalgroups(self):	
		globalgroups = []
		groups = self.groups.all()
		for g in groups:
			for gg in g.globalgroup_set.all():
				globalgroups.append(gg)
		return globalgroups

class Tag(models.Model):
	name = models.CharField(max_length=200)
	display_name = models.CharField(max_length=200,blank=True,null=True,default=None)
	ckan_id = models.CharField(max_length=200)
	translation = models.CharField(max_length=200,default=None, null=True,blank=True)
	load_round = models.ForeignKey(LoadRound, on_delete=models.CASCADE)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	datasets = models.ManyToManyField(Dataset, blank=True)
	similar_tags = models.ManyToManyField("self", blank=True)
	main_tag = models.BooleanField(default = 0)

	def __unicode__(self):
		return self.tagtranslation_set.first().translation if self.tagtranslation_set.count() > 0 else self.display_name

	def get_similar_tags(self,length=50,threshold=.0):
		srtd = sorted(self.tag_1_set.all(),reverse=True,key=lambda m: m.similarity)
		srtd = [x for x in srtd if x.similarity > threshold]
		return srtd[0:length]

	def cooc_vector(self):
		v = []
		for t in self.load_round.tag_set.all():
			try:
				c = Coocurrence.objects.get(tag_1 = self, tag_2 = t)
				v.append(c.value)
			except:
				v.append(0)
		return v

	def get_translation(self):
		return self.tagtranslation_set.first().translation if self.tagtranslation_set.count() > 0 else self.display_name

	def dataset_count(self):
		count = self.datasets.count()
		for s in self.similar_tags.all():
			if s.id != self.id:
				count += s.datasets.count()
		return count

class TagTranslation(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	translation = models.CharField(max_length=400,default=None, null=True,blank=True)

	def __unicode__(self):
		return self.translation

class TagMeaning(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	meaning = models.CharField(max_length=400,default=None, null=True,blank=True)

	def __unicode__(self):
		return self.meaning

class Coocurrence(models.Model):
	tag_1 = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name = 'tag_1_set')
	tag_2 = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name = 'tag_2_set')
	value = models.IntegerField(null=False,blank=False,default=0)
	similarity = models.FloatField(null=False,blank=False,default=0)
	def __unicode__(self):
		return self.tag_1.name + ' - ' + self.tag_2.name
		
class GlobalTag(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=1000, blank=True)
	tags = models.ManyToManyField(Tag, blank=True)
	uri = models.CharField(max_length=200, blank=True)
	narrower = models.ManyToManyField("self", blank=True,symmetrical=False,related_name='narrower_set')
	broader = models.ManyToManyField("self", blank=True,symmetrical=False,related_name='broader_set')
	related = models.ManyToManyField("self", blank=True,symmetrical=False,related_name='related_set')
	globalgroups = models.ManyToManyField(GlobalGroup, blank=True)
	insert_date = models.DateTimeField('insert date', default=datetime.now)

	def __unicode__(self):
		return self.name

	def dataset_count(self):
		datasets = []
		for t in self.tags.all():
			datasets += t.datasets.all()
		return len(set(datasets))

	def datasets(self):
		datasets = []
		for t in self.tags.all():
			datasets += t.datasets.all()
		return datasets


