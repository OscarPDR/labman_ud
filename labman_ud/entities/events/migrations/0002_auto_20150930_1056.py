# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventseealso',
            options={'verbose_name': 'Event (see also)', 'verbose_name_plural': 'Events (see also)'},
        ),
        migrations.AlterModelOptions(
            name='personrelatedtoevent',
            options={'verbose_name': 'Person related to Event', 'verbose_name_plural': 'People related to Events'},
        ),
    ]
