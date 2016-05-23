from django.db import models
from datetime import datetime
from numpy import array
from numpy import round
from django.db.models import Q
	
class Subject(models.Model):

	age = models.IntegerField(null=False,blank=False)
	internet_ability = models.IntegerField(null=True,blank=False)
	data_ability = models.IntegerField(null=True,blank=False)
	opendata_ability = models.IntegerField(null=True,blank=False)
	english_proficiency = models.IntegerField(null=True,blank=False, default = 0)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	usefulness = models.IntegerField(null=True,blank=False)
	usability = models.IntegerField(null=True,blank=False)
	comments = models.CharField(max_length=1000,null=True,blank=True)
	task_order = models.CharField(max_length=50,null=True,blank=True)
	search_method_order = models.CharField(max_length=50,null=True,blank=True)

	def __unicode__(self):
		return str(self.id) + ' - ' + str(self.usefulness) + ' - ' + str(self.usability)

	def average_time(self):
		d = DatasetAnswer.objects.filter(subject = self)
		t = array(map(lambda x: x.time(),d))
		return round(t.mean(),1), round(t.std(),1)

	def accepted_answers(self):
		a = float(len(Answer.objects.filter(dataset_answer__subject = self, confirmed = True)))
		b = len(Answer.objects.filter(dataset_answer__subject = self))
		if b:
			return round(a/b*100)
		else:
			return 0

class Task(models.Model):
	title = models.CharField(max_length=500) 
	description = models.CharField(max_length=5000) 	
	answer_fields = models.IntegerField(null=False,blank=False)	

	def average_time(self):
		d = DatasetAnswer.objects.filter(Q(task = self), ~Q(subject__usability = None))
		t = array(map(lambda x: x.time(),d))
		return round(t.mean(),1), round(t.std(),1)

	def accepted_answers(self):
		a = float(len(Answer.objects.filter(dataset_answer__task = self, confirmed = True)))
		b = len(Answer.objects.filter(Q(dataset_answer__task = self), ~Q(dataset_answer__subject__usability = None)))
		if b:
			return round(a/b*100)
		else:
			return 0

	def __str__(self):
		return self.title

class SearchMethod(models.Model):
	title = models.CharField(max_length=500) 
	description = models.CharField(max_length=5000)

	def __str__(self):
		return self.title

	def average_time(self):
		d = DatasetAnswer.objects.filter(Q(search_method = self), ~Q(subject__usability = None))
		t = array(map(lambda x: x.time(),d))
		return round(t.mean(),1), round(t.std(),1)

	def accepted_answers(self):
		a = float(len(Answer.objects.filter(dataset_answer__search_method = self, confirmed = True)))
		b = len(Answer.objects.filter(Q(dataset_answer__search_method = self), ~Q(dataset_answer__subject__usability = None)))
		return round(a/b*100)

class DatasetAnswer(models.Model):
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	search_method = models.ForeignKey(SearchMethod, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	urls = models.CharField(max_length=1000, blank = True, null = True)
	start_time = models.DateTimeField('start time',null=False,blank=False,default=0)
	end_time = models.DateTimeField('end time',null=False,blank=False,default=0)

	def __unicode__(self):
		return str(self.subject_id) + " - " + self.search_method.title + " - " + self.task.title

	def time(self):
		return (self.end_time - self.start_time).seconds

class Answer(models.Model):
	url = models.CharField(max_length=1000,null=True,blank=True,default=0)
	dataset_answer = models.ForeignKey(DatasetAnswer, on_delete=models.CASCADE)
	confirmed = models.BooleanField(default = False,null=False,blank=False)

	def __unicode__(self):
		return str(self.confirmed) + " - " + self.url
