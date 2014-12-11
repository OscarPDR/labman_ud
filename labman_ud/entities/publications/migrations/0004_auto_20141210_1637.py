# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import entities.publications.models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_auto_20141210_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranking',
            name='slug',
            field=models.SlugField(default='', unique=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coadvisor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coadvisor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationauthor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationauthor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationeditor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationeditor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationrank',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationrank',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationtag',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationtag',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ranking',
            name='icon',
            field=models.ImageField(null=True, upload_to=entities.publications.models.ranking_icon_picture_path, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ranking',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ranking',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesis',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesis',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisabstract',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisabstract',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vivapanel',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128934), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vivapanel',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 37, 22, 128988), auto_now=True),
            preserve_default=True,
        ),
    ]
