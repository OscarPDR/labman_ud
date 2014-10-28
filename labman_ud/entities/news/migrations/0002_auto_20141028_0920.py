# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('events', '0003_auto_20141028_0920'),
        ('news', '0001_initial'),
        ('persons', '0001_initial'),
        ('publications', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationrelatedtonews',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelatedtonews',
            name='news',
            field=models.ForeignKey(to='news.News'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelatedtonews',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personrelatedtonews',
            name='news',
            field=models.ForeignKey(to='news.News'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personrelatedtonews',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newstag',
            name='news',
            field=models.ForeignKey(to='news.News'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newstag',
            name='tag',
            field=models.ForeignKey(to='utils.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='persons',
            field=models.ManyToManyField(related_name=b'news', through='news.PersonRelatedToNews', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='projects',
            field=models.ManyToManyField(related_name=b'news', through='news.ProjectRelatedToNews', to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='publications',
            field=models.ManyToManyField(related_name=b'news', through='news.PublicationRelatedToNews', to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(related_name=b'news', through='news.NewsTag', to='utils.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventrelatedtonews',
            name='event',
            field=models.ForeignKey(to='events.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventrelatedtonews',
            name='news',
            field=models.ForeignKey(to='news.News'),
            preserve_default=True,
        ),
    ]
