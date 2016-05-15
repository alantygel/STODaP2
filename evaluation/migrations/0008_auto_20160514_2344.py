# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0007_auto_20160514_2342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='DatasetAnswer',
            new_name='dataset_answer',
        ),
    ]
