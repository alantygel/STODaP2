# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-04 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tag_analytics', '0009_auto_20160330_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagMeaning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meaning', models.CharField(blank=True, default=None, max_length=400, null=True)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tag_analytics.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='TagTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation', models.CharField(blank=True, default=None, max_length=400, null=True)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tag_analytics.Tag')),
            ],
        ),
    ]
