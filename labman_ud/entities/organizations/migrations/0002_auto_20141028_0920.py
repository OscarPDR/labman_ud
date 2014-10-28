# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='head',
            field=models.ForeignKey(blank=True, to='persons.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unit',
            name='organization',
            field=models.ForeignKey(related_name=b'unit', to='organizations.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationseealso',
            name='organization',
            field=models.ForeignKey(related_name=b'see_also_links', to='organizations.Organization'),
            preserve_default=True,
        ),
    ]
