# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('organizations', '0002_auto_20141028_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='country',
            field=models.ForeignKey(blank=True, to='utils.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='sub_organization_of',
            field=models.ForeignKey(blank=True, to='organizations.Organization', null=True),
            preserve_default=True,
        ),
    ]
