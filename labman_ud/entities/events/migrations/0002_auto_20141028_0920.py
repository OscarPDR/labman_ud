# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personrelatedtoevent',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventseealso',
            name='event',
            field=models.ForeignKey(to='events.Event'),
            preserve_default=True,
        ),
    ]
