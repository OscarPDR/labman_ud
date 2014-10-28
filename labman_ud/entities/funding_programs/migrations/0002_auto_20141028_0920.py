# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('organizations', '0002_auto_20141028_0920'),
        ('funding_programs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundingprogram',
            name='geographical_scope',
            field=models.ForeignKey(to='utils.GeographicalScope'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fundingprogram',
            name='organization',
            field=models.ForeignKey(to='organizations.Organization'),
            preserve_default=True,
        ),
    ]
