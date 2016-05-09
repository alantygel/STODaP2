# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='comments',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='search_method_order',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='task_order',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
