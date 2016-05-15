# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0005_subject_data_ability'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(default=0, max_length=1000, null=True, blank=True)),
                ('published', models.BooleanField(default=True)),
                ('DatasetAnswer', models.ForeignKey(to='evaluation.DatasetAnswer')),
            ],
        ),
    ]
