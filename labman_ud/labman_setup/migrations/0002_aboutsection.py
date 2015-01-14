# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('labman_setup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=50, blank=True)),
                ('icon_class', models.CharField(max_length=50)),
                ('order', models.PositiveSmallIntegerField(unique=True)),
                ('content', redactor.fields.RedactorField()),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
    ]
