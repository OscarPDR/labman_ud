# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20150416_0843'),
        ('persons', '0002_auto'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='projects',
            field=models.ManyToManyField(to='projects.Project', through='projects.AssignedPerson'),
            preserve_default=True,
        ),
    ]
