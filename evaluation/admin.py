from django.contrib import admin

from .models import Subject
from .models import Task
from .models import SearchMethod
from .models import DatasetAnswer
from .models import Answer

admin.site.register(Subject)
admin.site.register(Task)
admin.site.register(SearchMethod)
admin.site.register(DatasetAnswer)
admin.site.register(Answer)
