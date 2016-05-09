# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0004_auto_20160507_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='data_ability',
            field=models.IntegerField(null=True),
        ),
    ]
