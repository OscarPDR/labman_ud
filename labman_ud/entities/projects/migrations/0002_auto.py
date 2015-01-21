# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedPublication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
