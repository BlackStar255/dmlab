# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logcollector', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Logcollector',
            new_name='Log',
        ),
    ]
