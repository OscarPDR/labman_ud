# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0004_publication_zotero_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='co_advisors',
            field=models.ManyToManyField(related_name='coadvised_thesis', through='publications.CoAdvisor', to='persons.Person', blank=True),
        ),
    ]
