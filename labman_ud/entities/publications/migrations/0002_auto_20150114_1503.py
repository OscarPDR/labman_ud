# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesis',
            name='special_mention',
            field=models.CharField(max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coadvisor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coadvisor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationauthor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationauthor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationeditor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationeditor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationrank',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationrank',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationtag',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationtag',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ranking',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ranking',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesis',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesis',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisabstract',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisabstract',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vivapanel',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 357992), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vivapanel',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 14, 15, 3, 33, 358042), auto_now=True),
            preserve_default=True,
        ),
    ]
