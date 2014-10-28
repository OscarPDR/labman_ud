# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import datetime
import entities.persons.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('profile_id', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('position', models.CharField(max_length=250, blank=True)),
                ('description', models.TextField(max_length=2500, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nickname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('nickname', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=150, blank=True)),
            ],
            options={
                'ordering': ['nickname'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('first_name', models.CharField(max_length=25)),
                ('first_surname', models.CharField(max_length=50)),
                ('second_surname', models.CharField(max_length=50, null=True, blank=True)),
                ('full_name', models.CharField(max_length=150, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('biography', redactor.fields.RedactorField(null=True, blank=True)),
                ('safe_biography', models.TextField(max_length=2500, blank=True)),
                ('title', models.CharField(blank=True, max_length=15, choices=[(b'Dr.', b'Dr.')])),
                ('gender', models.CharField(blank=True, max_length=10, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('personal_website', models.URLField(max_length=250, blank=True)),
                ('email', models.EmailField(max_length=150, blank=True)),
                ('phone_number', models.CharField(max_length=25, blank=True)),
                ('phone_extension', models.CharField(max_length=10, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
                ('profile_picture', models.ImageField(null=True, upload_to=entities.persons.models.person_profile_picture_path, blank=True)),
                ('profile_konami_code_picture', models.ImageField(null=True, upload_to=entities.persons.models.person_profile_konami_code_picture_path, blank=True)),
                ('konami_code_position', models.CharField(max_length=150, blank=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonSeeAlso',
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
            name='PhDProgramFollowedByPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThesisRegisteredByPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('person', models.ForeignKey(to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
