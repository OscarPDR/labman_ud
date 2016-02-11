# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_project_private_participant_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=redactor.fields.RedactorField(max_length=7500, null=True, blank=True),
        ),
    ]
