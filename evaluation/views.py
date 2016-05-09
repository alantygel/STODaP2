from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from random import shuffle
import time    

from .models import Subject
from .models import Task
from .models import SearchMethod
from .models import DatasetAnswer

def index(request):
	template = loader.get_template('evaluation/index.html')
	return HttpResponse(template.render(None,request))

def entry_form(request):
	template = loader.get_template('evaluation/entry_form.html')
	return HttpResponse(template.render(None,request))


def initialize(request):
	s = Subject(age = request.POST['age'], 
			internet_ability = request.POST['internet_ability'], 
			data_ability = request.POST['data_ability'],
			opendata_ability = request.POST['open_data_ability'])
	tasks = Task.objects.all()
	tasks_id = map(lambda x: x.id, tasks)
	search_methods = SearchMethod.objects.all()
	search_methods_id = map(lambda x: x.id, search_methods)

	shuffle(tasks_id)
	shuffle(search_methods_id)

	s.task_order = '#'.join([str(i) for i in tasks_id])
	s.search_method_order = '#'.join([str(i) for i in search_methods_id])
	s.save()

	task = Task.objects.get(id = s.task_order.split('#')[0])
	search_method = SearchMethod.objects.get(id = s.search_method_order.split('#')[0])
	context = {
		'id' : s.id,
		'task_number' : 0,
		'task_p1' : 1,
		'task' : task,
		'search_method' : search_method,
		'answer_fields' : range(task.answer_fields),
		'start_time' : time.strftime('%Y-%m-%d %H:%M:%S')
	}

	template = loader.get_template('evaluation/show_task.html')
	return HttpResponse(template.render(context,request))

def show_task(request):
	sid = request.POST['subject']
	task_number = request.POST['task_number']
	start_time = request.POST['start_time']

	s = Subject.objects.get(id = sid)
	task = Task.objects.get(id = s.task_order.split('#')[int(task_number)])
	search_method = SearchMethod.objects.get(id = s.search_method_order.split('#')[int(task_number)])

	urls = "#".join(request.POST.getlist('url'))
	t = DatasetAnswer(urls = urls, subject = s, task = task, 
		search_method = search_method, start_time = start_time, end_time = time.strftime('%Y-%m-%d %H:%M:%S'))
	t.save()

	if int(task_number) < 2:

		task_number = int(task_number) + 1
		task = Task.objects.get(id = s.task_order.split('#')[task_number])
		search_method = SearchMethod.objects.get(id = s.search_method_order.split('#')[task_number])

		context = {
			'id' : sid,
			'task_number' : task_number,
			'task_p1' : task_number+1,
			'task' : task,
			'search_method' : search_method,
			'answer_fields' : range(task.answer_fields),
			'start_time' : time.strftime('%Y-%m-%d %H:%M:%S'),
		}
	
		template = loader.get_template('evaluation/show_task.html')
		return HttpResponse(template.render(context,request))
	else:
		context = { 'id' : sid }
		template = loader.get_template('evaluation/eval_form.html')
		return HttpResponse(template.render(context,request))

def finish(request):
	sid = request.POST['subject']
	s = Subject.objects.get(id = sid)
	s.usability = request.POST['usability']
	s.usefulness = request.POST['usefulness']
	s.comments = request.POST['comments']
	s.save()

	template = loader.get_template('evaluation/thankyou.html')
	return HttpResponse(template.render(None,request))
