# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('urls', models.CharField(max_length=1000)),
                ('start_time', models.DateTimeField(default=0, verbose_name=b'start time')),
                ('end_time', models.DateTimeField(default=0, verbose_name=b'end time')),
            ],
        ),
        migrations.CreateModel(
            name='SearchMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField()),
                ('internet_ability', models.IntegerField(null=True)),
                ('opendata_ability', models.IntegerField(null=True)),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'insert date')),
                ('satisfaction', models.IntegerField(null=True)),
                ('usability', models.IntegerField(null=True)),
                ('comments', models.CharField(max_length=1000)),
                ('task_order', models.CharField(max_length=50)),
                ('search_method_order', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=5000)),
                ('answer_fields', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='datasetanswer',
            name='search_method',
            field=models.ForeignKey(to='evaluation.SearchMethod'),
        ),
        migrations.AddField(
            model_name='datasetanswer',
            name='subject',
            field=models.ForeignKey(to='evaluation.Subject'),
        ),
        migrations.AddField(
            model_name='datasetanswer',
            name='task',
            field=models.ForeignKey(to='evaluation.Task'),
        ),
    ]
