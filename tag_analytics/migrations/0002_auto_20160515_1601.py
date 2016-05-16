# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tag_analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalgroup',
            name='number_of_datasets',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='globaltag',
            name='number_of_datasets',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
