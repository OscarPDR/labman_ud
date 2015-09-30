# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_language_language_tag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['slug'], 'verbose_name': 'City', 'verbose_name_plural': 'Cities'},
        ),
    ]
