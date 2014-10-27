# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logcollector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.BigIntegerField()),
                ('dim1', models.IntegerField()),
                ('dim2', models.IntegerField()),
                ('value', models.FloatField()),
            ],
            options={
                'ordering': ('timestamp',),
            },
            bases=(models.Model,),
        ),
    ]
