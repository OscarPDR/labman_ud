# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('events', '0002_auto_20141028_0920'),
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='host_city',
            field=models.ForeignKey(blank=True, to='utils.City', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='host_country',
            field=models.ForeignKey(blank=True, to='utils.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='proceedings',
            field=models.ForeignKey(related_name=b'conference', blank=True, to='publications.Proceedings', null=True),
            preserve_default=True,
        ),
    ]
