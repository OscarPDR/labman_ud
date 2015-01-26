# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto'),
        ('publications', '0003_auto'),
        ('events', '__first__'),
        ('projects', '0004_auto'),
        ('persons', '0002_auto'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRelatedToNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='events.Event')),
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
                ('post_tweet', models.BooleanField(default=False)),
                ('tweet_cc', models.CharField(max_length=70, null=True, blank=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('content', redactor.fields.RedactorField()),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('city', models.ForeignKey(blank=True, to='utils.City', null=True)),
                ('country', models.ForeignKey(blank=True, to='utils.Country', null=True)),
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
                ('news', models.ForeignKey(to='news.News')),
                ('tag', models.ForeignKey(to='utils.Tag')),
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
                ('news', models.ForeignKey(to='news.News')),
                ('person', models.ForeignKey(to='persons.Person')),
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
                ('news', models.ForeignKey(to='news.News')),
                ('project', models.ForeignKey(to='projects.Project')),
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
                ('news', models.ForeignKey(to='news.News')),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='news',
            name='persons',
            field=models.ManyToManyField(related_name='news', through='news.PersonRelatedToNews', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='projects',
            field=models.ManyToManyField(related_name='news', through='news.ProjectRelatedToNews', to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='publications',
            field=models.ManyToManyField(related_name='news', through='news.PublicationRelatedToNews', to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(related_name='news', through='news.NewsTag', to='utils.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventrelatedtonews',
            name='news',
            field=models.ForeignKey(to='news.News'),
            preserve_default=True,
        ),
    ]
