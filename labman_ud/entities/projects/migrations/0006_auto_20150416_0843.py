# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20150126_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assigned_people',
            field=models.ManyToManyField(related_name='assigned_projects', through='projects.AssignedPerson', to='persons.Person'),
            preserve_default=True,
        ),
    ]
