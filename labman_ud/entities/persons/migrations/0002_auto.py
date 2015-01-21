# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 41, 41, 416201), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 41, 41, 416252), auto_now=True)),
                ('position', models.CharField(max_length=250, blank=True)),
                ('description', models.TextField(max_length=2500, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('organization', models.ForeignKey(to='organizations.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='job',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
    ]
