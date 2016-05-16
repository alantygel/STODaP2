# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0008_auto_20160514_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='english_proficiency',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
