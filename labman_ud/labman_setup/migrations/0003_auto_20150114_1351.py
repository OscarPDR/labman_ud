# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labman_setup', '0002_aboutsection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutsection',
            name='icon_class',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
