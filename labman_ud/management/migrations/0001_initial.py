# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgnoredSimilarNames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 14, 10, 3, 59, 803624), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 14, 10, 3, 59, 803668), auto_now=True)),
                ('test_person', models.ForeignKey(related_name='test_person', to='persons.Person')),
                ('testing_person', models.ForeignKey(related_name='testing_person', to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
