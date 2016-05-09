from django.db import models
from datetime import datetime
	
class Subject(models.Model):

	age = models.IntegerField(null=False,blank=False)
	internet_ability = models.IntegerField(null=True,blank=False)
	data_ability = models.IntegerField(null=True,blank=False)
	opendata_ability = models.IntegerField(null=True,blank=False)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	usefulness = models.IntegerField(null=True,blank=False)
	usability = models.IntegerField(null=True,blank=False)
	comments = models.CharField(max_length=1000,null=True,blank=True)
	task_order = models.CharField(max_length=50,null=True,blank=True)
	search_method_order = models.CharField(max_length=50,null=True,blank=True)

	def __str__(self):
		return str(self.id)

class Task(models.Model):
	title = models.CharField(max_length=500) 
	description = models.CharField(max_length=5000) 	
	answer_fields = models.IntegerField(null=False,blank=False)	

	def __str__(self):
		return self.title

class SearchMethod(models.Model):
	title = models.CharField(max_length=500) 
	description = models.CharField(max_length=5000)

	def __str__(self):
		return self.title

class DatasetAnswer(models.Model):
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	search_method = models.ForeignKey(SearchMethod, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	urls = models.CharField(max_length=1000)
	start_time = models.DateTimeField('start time',null=False,blank=False,default=0)
	end_time = models.DateTimeField('end time',null=False,blank=False,default=0)

	def __unicode__(self):
		return self.urls
