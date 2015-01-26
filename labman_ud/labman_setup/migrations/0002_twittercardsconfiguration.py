# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import labman_setup.models


class Migration(migrations.Migration):

    dependencies = [
        ('labman_setup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterCardsConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_account', models.CharField(max_length=50, null=True, blank=True)),
                ('card_title', models.CharField(max_length=70)),
                ('card_description', models.CharField(max_length=200)),
                ('card_image', models.ImageField(null=True, upload_to=labman_setup.models.twitter_card_picture_path, blank=True)),
                ('base_url', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
