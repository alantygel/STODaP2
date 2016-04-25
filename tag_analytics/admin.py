from django.contrib import admin

from .models import OpenDataPortal
from .models import LoadRound
from .models import Tag
from .models import GlobalTag
from .models import Dataset
from .models import Group
from .models import GlobalGroup
from .models import ODPMetadata

admin.site.register(OpenDataPortal)
admin.site.register(LoadRound)
admin.site.register(Tag)
admin.site.register(GlobalTag)
admin.site.register(Dataset)
admin.site.register(Group)
admin.site.register(GlobalGroup)
admin.site.register(ODPMetadata)
