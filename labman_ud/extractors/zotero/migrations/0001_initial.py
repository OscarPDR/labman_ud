# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_auto_20141028_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZoteroExtractorLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('item_key', models.CharField(max_length=50)),
                ('version', models.PositiveIntegerField()),
                ('publication', models.ForeignKey(related_name=b'zotero_extractor_logs', default=None, blank=True, to='publications.Publication', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
