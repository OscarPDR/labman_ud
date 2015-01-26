# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import entities.funding_programs.models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundingProgram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=250)),
                ('short_name', models.CharField(max_length=250, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('observations', models.TextField(max_length=1000, null=True, blank=True)),
                ('geographical_scope', models.ForeignKey(to='utils.GeographicalScope')),
                ('organization', models.ForeignKey(to='organizations.Organization')),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FundingProgramLogo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('logo', models.ImageField(max_length=250, null=True, upload_to=entities.funding_programs.models.funding_program_logo_path, blank=True)),
                ('funding_program', models.ForeignKey(to='funding_programs.FundingProgram')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FundingProgramSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('funding_program', models.ForeignKey(to='funding_programs.FundingProgram')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
