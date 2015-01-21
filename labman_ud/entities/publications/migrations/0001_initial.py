# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import datetime
import django.core.validators
import entities.publications.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoAdvisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
            ],
            options={
                'verbose_name': 'Co-advisor',
                'verbose_name_plural': 'Co-advisors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('abstract', models.TextField(max_length=2500, null=True, blank=True)),
                ('doi', models.CharField(max_length=100, null=True, verbose_name='DOI', blank=True)),
                ('published', models.DateField(null=True, blank=True)),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1950), django.core.validators.MaxValueValidator(2080)])),
                ('pdf', models.FileField(max_length=1000, null=True, upload_to=entities.publications.models.publication_path, blank=True)),
                ('bibtex', models.TextField(max_length=2500, null=True, blank=True)),
                ('child_type', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'ordering': ['-slug'],
                'verbose_name': 'Publication',
                'verbose_name_plural': 'Publications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Publication author',
                'verbose_name_plural': 'Publication authors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationEditor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
            ],
            options={
                'verbose_name': 'Publication editor',
                'verbose_name_plural': 'Publication editors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
            ],
            options={
                'ordering': ['publication__title'],
                'verbose_name': 'Publication ranking',
                'verbose_name_plural': 'Publication rankings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('see_also', models.URLField(max_length=512)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
            ],
            options={
                'ordering': ['tag__slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('icon', models.ImageField(null=True, upload_to=entities.publications.models.ranking_icon_picture_path, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Ranking',
                'verbose_name_plural': 'Rankings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('title', models.CharField(max_length=1000)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('registration_date', models.DateField(null=True, blank=True)),
                ('year', models.PositiveIntegerField()),
                ('pdf', models.FileField(null=True, upload_to=entities.publications.models.thesis_path, blank=True)),
                ('number_of_pages', models.PositiveIntegerField(null=True, blank=True)),
                ('viva_date', models.DateTimeField()),
                ('viva_outcome', models.CharField(default=b'Apt', max_length=250, blank=True, choices=[(b'Apt', b'Apt'), (b'Cum Laude', b'Cum Laude'), (b'Cum Laude by unanimity', b'Cum Laude by unanimity')])),
                ('special_mention', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'ordering': ['slug'],
                'verbose_name': 'Thesis',
                'verbose_name_plural': 'Theses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThesisAbstract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271519), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 14, 40, 42, 271567), auto_now=True)),
                ('abstract', redactor.fields.RedactorField(max_length=5000, blank=True)),
            ],
            options={
                'verbose_name': 'Thesis abstract',
                'verbose_name_plural': 'Thesis abstracts',
            },
            bases=(models.Model,),
        ),
    ]
