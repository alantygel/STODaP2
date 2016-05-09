# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0002_auto_20160507_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='satisfaction',
            new_name='usefulnes',
        ),
    ]
