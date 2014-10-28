# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_auto_20141028_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coadvisor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='coadvisor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='publicationauthor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='publicationauthor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='publicationeditor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='publicationeditor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='publicationseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='publicationseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='publicationtag',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='publicationtag',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='thesisabstract',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='thesisabstract',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='thesisseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='thesisseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='vivapanel',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='vivapanel',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
    ]
