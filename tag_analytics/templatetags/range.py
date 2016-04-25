from django import template
register = template.Library()

@register.filter
def range(List, i):
	r = i.split("#")
	return List[int(r[0]):int(r[1])]
