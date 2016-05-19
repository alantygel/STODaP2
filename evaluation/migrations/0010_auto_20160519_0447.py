# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0009_subject_english_proficiency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetanswer',
            name='urls',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
