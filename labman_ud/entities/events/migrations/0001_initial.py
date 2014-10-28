# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import entities.events.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('event_type', models.CharField(default=b'Generic event', max_length=75, choices=[(b'Academic event', b'Academic event'), (b'Generic event', b'Generic event'), (b'Hackathon', b'Hackathon'), (b'Project meeting', b'Project meeting')])),
                ('full_name', models.CharField(max_length=250)),
                ('short_name', models.CharField(max_length=250, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('location', models.CharField(max_length=250, null=True, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('year', models.PositiveIntegerField()),
                ('homepage', models.URLField(null=True, verbose_name=b'Homepage', blank=True)),
                ('description', models.TextField(max_length=1500, blank=True)),
                ('observations', models.TextField(max_length=1500, blank=True)),
                ('logo', models.ImageField(upload_to=entities.events.models.event_logo_path, null=True, verbose_name=b'Logo', blank=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('see_also', models.URLField(max_length=512)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonRelatedToEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
