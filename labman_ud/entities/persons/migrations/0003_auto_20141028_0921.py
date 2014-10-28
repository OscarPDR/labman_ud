# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20141028_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountprofile',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='accountprofile',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='nickname',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='nickname',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='personseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='personseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='phdprogramfollowedbyperson',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='phdprogramfollowedbyperson',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
        migrations.AlterField(
            model_name='thesisregisteredbyperson',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703336), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='thesisregisteredbyperson',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 9, 21, 8, 703383), auto_now=True),
        ),
    ]
