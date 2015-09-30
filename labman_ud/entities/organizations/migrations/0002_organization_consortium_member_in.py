# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20150416_0843'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='consortium_member_in',
            field=models.ManyToManyField(related_name='organizations', through='projects.ConsortiumMember', to='projects.Project'),
        ),
    ]
