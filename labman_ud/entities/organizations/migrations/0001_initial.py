# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import entities.organizations.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('organization_type', models.CharField(default=b'Enterprise', max_length=75, choices=[(b'Association', b'Association'), (b'Educational organization', b'Educational organization'), (b'Enterprise', b'Enterprise'), (b'Foundation', b'Foundation'), (b'Public administration', b'Public administration'), (b'Research group', b'Research group'), (b'University', b'University')])),
                ('full_name', models.CharField(max_length=250)),
                ('short_name', models.CharField(max_length=250, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('homepage', models.URLField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=entities.organizations.models.organization_logo_path, blank=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationSeeAlso',
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
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('order', models.PositiveSmallIntegerField(unique=True)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
    ]
