# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0006_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='published',
        ),
        migrations.AddField(
            model_name='answer',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
