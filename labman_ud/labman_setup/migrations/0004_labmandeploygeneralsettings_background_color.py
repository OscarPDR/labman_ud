# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labman_setup', '0003_googlesearchscript'),
    ]

    operations = [
        migrations.AddField(
            model_name='labmandeploygeneralsettings',
            name='background_color',
            field=models.CharField(max_length=25, null=True, blank=True),
            preserve_default=True,
        ),
    ]
