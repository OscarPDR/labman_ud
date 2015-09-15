# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labman_setup', '0004_labmandeploygeneralsettings_background_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labmandeploygeneralsettings',
            name='email_address',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
