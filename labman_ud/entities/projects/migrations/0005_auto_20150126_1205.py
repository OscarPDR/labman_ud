# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=redactor.fields.RedactorField(max_length=3000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
