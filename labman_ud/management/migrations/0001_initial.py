# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0003_auto_20141028_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgnoredSimilarNames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True)),
                ('test_person', models.ForeignKey(related_name=b'test_person', to='persons.Person')),
                ('testing_person', models.ForeignKey(related_name=b'testing_person', to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
