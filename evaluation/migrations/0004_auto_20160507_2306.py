# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0003_auto_20160507_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='usefulnes',
            new_name='usefulness',
        ),
    ]
