# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20150416_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='private_participant_details',
            field=models.BooleanField(default=False),
        ),
    ]
