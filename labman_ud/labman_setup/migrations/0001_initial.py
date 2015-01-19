# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import labman_setup.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabmanDeployGeneralSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('favicon', models.ImageField(null=True, upload_to=labman_setup.models.favicon_picture_path, blank=True)),
                ('research_group_full_name', models.CharField(max_length=75)),
                ('research_group_short_name', models.CharField(max_length=75, null=True, blank=True)),
                ('research_group_team_image', models.ImageField(null=True, upload_to=labman_setup.models.team_picture_path, blank=True)),
                ('research_group_official_logo', models.ImageField(null=True, upload_to=labman_setup.models.official_logo_picture_path, blank=True)),
                ('research_group_description', redactor.fields.RedactorField()),
                ('address', redactor.fields.RedactorField(null=True, blank=True)),
                ('map_external_link', models.URLField(null=True, blank=True)),
                ('phone_number', models.CharField(max_length=25, null=True, blank=True)),
                ('phone_extension', models.CharField(max_length=25, null=True, blank=True)),
                ('email_address', models.EmailField(max_length=75, null=True, blank=True)),
                ('contact_person', models.CharField(max_length=75, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OfficialSocialProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('network_image', models.ImageField(upload_to=labman_setup.models.official_network_picture_path)),
                ('profile_link', models.URLField()),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=50, blank=True)),
                ('help_text', models.CharField(max_length=75, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SEOAndAnalytics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta_keywords', models.TextField(max_length=750, null=True, blank=True)),
                ('meta_description', models.TextField(max_length=750, null=True, blank=True)),
                ('google_analytics_account', models.CharField(max_length=25, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TweetPonyConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consumer_key', models.CharField(max_length=100)),
                ('consumer_secret', models.CharField(max_length=100)),
                ('access_token', models.CharField(max_length=100)),
                ('access_token_secret', models.CharField(max_length=100)),
                ('http_proxy', models.CharField(max_length=150, null=True, blank=True)),
                ('https_proxy', models.CharField(max_length=150, null=True, blank=True)),
                ('karmacracy_username', models.CharField(max_length=75, null=True, blank=True)),
                ('karmacracy_api_key', models.CharField(max_length=75, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ZoteroConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_url', models.CharField(default='https://api.zotero.org', max_length=50)),
                ('library_type', models.CharField(default='group', max_length=10)),
                ('api_key', models.CharField(max_length=50)),
                ('library_id', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
