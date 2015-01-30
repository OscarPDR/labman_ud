# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import entities.persons.models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('publications', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_id', models.CharField(max_length=150)),
                ('network', models.ForeignKey(to='utils.Network')),
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
                ('publications', models.ManyToManyField(to='publications.Publication', through='publications.PublicationAuthor')),
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
                ('see_also', models.URLField(max_length=512)),
                ('person', models.ForeignKey(related_name='see_also_links', to='persons.Person')),
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
                ('person', models.ForeignKey(to='persons.Person')),
                ('thesis', models.ForeignKey(to='publications.Thesis')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nickname',
            name='person',
            field=models.ForeignKey(related_name='nicknames', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
    ]
