# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_auto'),
        ('projects', '0002_auto'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatedpublication',
            name='publication',
            field=models.ForeignKey(related_name='projects', to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttag',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
    ]
