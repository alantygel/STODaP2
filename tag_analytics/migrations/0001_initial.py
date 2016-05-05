# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coocurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(default=0)),
                ('similarity', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000, null=True, blank=True)),
                ('display_name', models.CharField(max_length=200, null=True, blank=True)),
                ('ckan_id', models.CharField(max_length=200)),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='insert date')),
                ('metadata_modified', models.DateTimeField(default=None, null=True, verbose_name='metadata_modified', blank=True)),
                ('n_tags', models.IntegerField(null=True, blank=True)),
                ('n_resources', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('uri', models.CharField(max_length=400, blank=True)),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='insert date')),
            ],
        ),
        migrations.CreateModel(
            name='GlobalTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000, blank=True)),
                ('uri', models.CharField(max_length=200, blank=True)),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='insert date')),
                ('broader', models.ManyToManyField(related_name='broader_set', to='tag_analytics.GlobalTag', blank=True)),
                ('globalgroups', models.ManyToManyField(to='tag_analytics.GlobalGroup', blank=True)),
                ('narrower', models.ManyToManyField(related_name='narrower_set', to='tag_analytics.GlobalTag', blank=True)),
                ('related', models.ManyToManyField(related_name='related_set', to='tag_analytics.GlobalTag', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('display_name', models.CharField(max_length=200, null=True, blank=True)),
                ('ckan_id', models.CharField(max_length=200)),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='insert date')),
                ('n_packages', models.IntegerField(default=0, null=True, blank=True)),
                ('translation', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoadRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roundn', models.IntegerField()),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='insert date')),
                ('success', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ODPMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_title', models.CharField(max_length=200, null=True, blank=True)),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='insert date')),
                ('ckan_version', models.CharField(max_length=200, null=True, blank=True)),
                ('site_description', models.CharField(max_length=2000, null=True, blank=True)),
                ('locale_default', models.CharField(max_length=10, null=True, blank=True)),
                ('n_packages', models.IntegerField(default=0, null=True, blank=True)),
                ('load_round', models.ForeignKey(to='tag_analytics.LoadRound')),
            ],
        ),
        migrations.CreateModel(
            name='OpenDataPortal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=200)),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='insert date')),
                ('published', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('display_name', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('ckan_id', models.CharField(max_length=200)),
                ('translation', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('insert_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='insert date')),
                ('main_tag', models.BooleanField(default=0)),
                ('datasets', models.ManyToManyField(to='tag_analytics.Dataset', blank=True)),
                ('load_round', models.ForeignKey(to='tag_analytics.LoadRound')),
                ('similar_tags', models.ManyToManyField(related_name='similar_tags_rel_+', to='tag_analytics.Tag', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TagMeaning',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meaning', models.CharField(default=None, max_length=400, null=True, blank=True)),
                ('tag', models.ForeignKey(to='tag_analytics.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='TagTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('translation', models.CharField(default=None, max_length=400, null=True, blank=True)),
                ('tag', models.ForeignKey(to='tag_analytics.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='loadround',
            name='open_data_portal',
            field=models.ForeignKey(to='tag_analytics.OpenDataPortal'),
        ),
        migrations.AddField(
            model_name='group',
            name='load_round',
            field=models.ForeignKey(to='tag_analytics.LoadRound'),
        ),
        migrations.AddField(
            model_name='globaltag',
            name='tags',
            field=models.ManyToManyField(to='tag_analytics.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='globalgroup',
            name='groups',
            field=models.ManyToManyField(to='tag_analytics.Group', blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='groups',
            field=models.ManyToManyField(to='tag_analytics.Group', blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='load_round',
            field=models.ForeignKey(to='tag_analytics.LoadRound'),
        ),
        migrations.AddField(
            model_name='coocurrence',
            name='tag_1',
            field=models.ForeignKey(related_name='tag_1_set', to='tag_analytics.Tag'),
        ),
        migrations.AddField(
            model_name='coocurrence',
            name='tag_2',
            field=models.ForeignKey(related_name='tag_2_set', to='tag_analytics.Tag'),
        ),
    ]
