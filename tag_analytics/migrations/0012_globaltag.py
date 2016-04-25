# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-11 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag_analytics', '0011_globalgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('tags', models.ManyToManyField(blank=True, to='tag_analytics.Tag')),
            ],
        ),
    ]
