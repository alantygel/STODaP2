from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from random import shuffle
import time    
from django.views import generic

from .models import Subject
from .models import Task
from .models import SearchMethod
from .models import DatasetAnswer
from .models import Answer

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
			opendata_ability = request.POST['open_data_ability'],
			english_proficiency = request.POST['english_proficiency'],)

	last = Subject.objects.last()
	to = last.task_order.split("#")	
	to = to[1:] + to[:1]
	# to = to[1:] + to[:1]
	so = last.search_method_order.split("#")
	# so = so[1:] + so[:1]

	ordering = range(len(so))
	shuffle(ordering)

	tasks_id  = []; search_methods_id = []
	for i in range(len(so)):
		tasks_id.append(to[ordering[i]])
		search_methods_id.append(so[ordering[i]])

	# tasks = Task.objects.all()
	# tasks_id = map(lambda x: x.id, tasks)
	# search_methods = SearchMethod.objects.all()
	# search_methods_id = map(lambda x: x.id, search_methods)

	# shuffle(tasks_id)
	# shuffle(search_methods_id)

	s.task_order = '#'.join(tasks_id)
	s.search_method_order = '#'.join(search_methods_id)
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
	t = DatasetAnswer(subject = s, task = task, 
		search_method = search_method, start_time = start_time, end_time = time.strftime('%Y-%m-%d %H:%M:%S'))
	t.save()

	for url in request.POST.getlist('url'):
		a = Answer(url = url, dataset_answer = t)
		a.save()

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

#### RESULTS #####

def quest_answers(request):
	subjects = Subject.objects.all()
	tasks = Task.objects.all()
	search_methods = SearchMethod.objects.all()
	dataset_answers = DatasetAnswer.objects.all()
	context = {
		'subjects' : subjects,
		'search_methods' : search_methods,
		'tasks' : tasks,
		'dataset_answers' : dataset_answers
		}
	template = loader.get_template('evaluation/quest_answers.html')
	return HttpResponse(template.render(context,request))

class SubjectDetailView(generic.DetailView):
	model = Subject
	template_name = 'evaluation/subject.html'

def subject_edit(request):
	answers = Answer.objects.filter(dataset_answer__subject_id = request.POST['s_id'])

	for a in answers:
		try:
			v = request.POST[str(a.id)]
			a.confirmed = True
		except:
			a.confirmed = False
		a.save()
	subjects = Subject.objects.all()
	context = {
		'subjects' : subjects
	}

	template = loader.get_template('evaluation/subjects.html')
	return HttpResponse(template.render(context,request))