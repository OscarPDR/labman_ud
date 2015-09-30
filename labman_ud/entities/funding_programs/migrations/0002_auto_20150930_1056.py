# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funding_programs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fundingprogram',
            options={'ordering': ['slug'], 'verbose_name': 'Funding program', 'verbose_name_plural': 'Funding programs'},
        ),
    ]
