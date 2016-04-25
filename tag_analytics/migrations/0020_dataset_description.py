# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tag_analytics', '0017_auto_20160419_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='description',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
