# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventRelatedToNews',
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
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('content', redactor.fields.RedactorField()),
                ('created', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsTag',
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
            name='PersonRelatedToNews',
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
            name='ProjectRelatedToNews',
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
            name='PublicationRelatedToNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922542), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 20, 5, 922590), auto_now=True)),
                ('news', models.ForeignKey(to='news.News')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
