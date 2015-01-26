# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgnoredSimilarNames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_person', models.ForeignKey(related_name='test_person', to='persons.Person')),
                ('testing_person', models.ForeignKey(related_name='testing_person', to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
