import datetime
from django import template
from evaluation.models import Subject, Task, SearchMethod, DatasetAnswer, Answer
from numpy import array, median, round, mean, std
from django.db.models import Q

register = template.Library()

@register.simple_tag
def tct(sm, t, opt = 0):

	if sm == None:
		dataset_answers = DatasetAnswer.objects.filter(task = t)
	elif t == None:
		dataset_answers = DatasetAnswer.objects.filter(search_method = sm)
	else:
		dataset_answers = DatasetAnswer.objects.filter(search_method = sm, task = t)

	dataset_answers = filter(lambda x: x.valid() == True, dataset_answers)

	if opt == 0:
		time = array(map(lambda x: x.time()[0], dataset_answers))
		n = sum(map(lambda x: x.time()[1], dataset_answers))
	elif opt == 1:
		time = array(map(lambda x: x.time_notnull()[0], dataset_answers))
		n = sum(map(lambda x: x.time_notnull()[1], dataset_answers))
	else:
		time = array(map(lambda x: x.time_correct()[0], dataset_answers))
		n = sum(map(lambda x: x.time_correct()[1], dataset_answers))

	return str(int(round(median(time)))) + " $\pm$ " + str(int(round(std(time)))) + " ("+ str(int(n)) + ")"