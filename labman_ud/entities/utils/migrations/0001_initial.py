# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import datetime
import entities.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('full_name', models.CharField(max_length=150)),
                ('short_name', models.CharField(max_length=150, blank=True)),
                ('slug', models.SlugField(max_length=150, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, null=True, blank=True)),
                ('description', redactor.fields.RedactorField()),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContributionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
                ('description', models.TextField(max_length=1500, blank=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('full_name', models.CharField(max_length=150)),
                ('short_name', models.CharField(max_length=150, blank=True)),
                ('slug', models.SlugField(max_length=150, blank=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, null=True, blank=True)),
                ('description', models.TextField(max_length=1500, blank=True)),
                ('logo', models.FileField(null=True, upload_to=entities.utils.models.file_path, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeographicalScope',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, blank=True)),
                ('description', models.TextField(max_length=1500, blank=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('full_name', models.CharField(max_length=150)),
                ('short_name', models.CharField(max_length=50, null=True, blank=True)),
                ('slug', models.SlugField(max_length=150, null=True, blank=True)),
                ('license_url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('base_url', models.URLField(max_length=250)),
                ('slug', models.SlugField(max_length=150, blank=True)),
                ('icon', models.ImageField(null=True, upload_to=entities.utils.models.network_icon_path, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonRelatedToTalkOrCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('person', models.ForeignKey(to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhDProgram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('name', models.CharField(max_length=500)),
                ('homepage', models.URLField(max_length=250)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('faculty', models.ForeignKey(related_name='faculty_holding_a_phd_program', blank=True, to='organizations.Organization')),
                ('university', models.ForeignKey(related_name='university_holding_a_phd_program', to='organizations.Organization')),
            ],
            options={
                'verbose_name': 'PhD program',
                'verbose_name_plural': 'PhD programs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectRelatedToTalkOrCourse',
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
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(max_length=100, blank=True)),
                ('description', models.TextField(max_length=1500, blank=True)),
                ('exclude_from_charts', models.BooleanField(default=False)),
                ('relevance_order', models.PositiveSmallIntegerField(default=0)),
                ('rgb_color', models.CharField(max_length=6, null=True, verbose_name='RGB color (#)', blank=True)),
            ],
            options={
                'ordering': ['relevance_order'],
            },
            bases=(models.Model,),
        ),
    ]
