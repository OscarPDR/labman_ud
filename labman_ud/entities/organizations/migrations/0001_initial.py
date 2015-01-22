# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import entities.organizations.models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization_type', models.CharField(default=b'Enterprise', max_length=75, choices=[(b'Association', b'Association'), (b'Educational organization', b'Educational organization'), (b'Enterprise', b'Enterprise'), (b'Foundation', b'Foundation'), (b'Public administration', b'Public administration'), (b'Research group', b'Research group'), (b'University', b'University')])),
                ('full_name', models.CharField(max_length=250)),
                ('short_name', models.CharField(max_length=250, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('homepage', models.URLField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=entities.organizations.models.organization_logo_path, blank=True)),
                ('country', models.ForeignKey(blank=True, to='utils.Country', null=True)),
                ('sub_organization_of', models.ForeignKey(blank=True, to='organizations.Organization', null=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('organization', models.ForeignKey(related_name='see_also_links', to='organizations.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField(unique=True)),
                ('head', models.ForeignKey(blank=True, to='persons.Person', null=True)),
                ('organization', models.ForeignKey(related_name='unit', to='organizations.Organization')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
    ]
