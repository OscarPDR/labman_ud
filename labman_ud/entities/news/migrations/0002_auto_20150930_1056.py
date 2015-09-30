# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventrelatedtonews',
            options={'verbose_name': 'Event related to News piece', 'verbose_name_plural': 'Events related to News pieces'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-created',), 'verbose_name': 'News piece', 'verbose_name_plural': 'News pieces'},
        ),
        migrations.AlterModelOptions(
            name='newstag',
            options={'verbose_name': 'News Tag', 'verbose_name_plural': 'News Tags'},
        ),
        migrations.AlterModelOptions(
            name='personrelatedtonews',
            options={'verbose_name': 'Person related to News piece', 'verbose_name_plural': 'People related to News pieces'},
        ),
        migrations.AlterModelOptions(
            name='projectrelatedtonews',
            options={'verbose_name': 'Project related to News piece', 'verbose_name_plural': 'Projects related to News pieces'},
        ),
        migrations.AlterModelOptions(
            name='publicationrelatedtonews',
            options={'verbose_name': 'Publication related to News piece', 'verbose_name_plural': 'Publications related to News pieces'},
        ),
    ]
