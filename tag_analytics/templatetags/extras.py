from django import template
from django.template import Variable, VariableDoesNotExist
from time import time

register = template.Library()

@register.filter(name='get_class')
def get_class(value):
	return value.__class__.__name__

@register.assignment_tag()
def resolve(lookup, target):
    try:
        return Variable(lookup).resolve(target)
    except VariableDoesNotExist:
        return None

@register.simple_tag
def print_time():
    return time()
