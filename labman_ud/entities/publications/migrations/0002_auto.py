# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '__first__'),
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proceedings',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('publisher', models.CharField(max_length=250, null=True, blank=True)),
                ('place', models.CharField(max_length=300, null=True, blank=True)),
                ('volume', models.CharField(max_length=300, null=True, blank=True)),
                ('isbn', models.CharField(max_length=100, null=True, verbose_name='ISBN', blank=True)),
                ('series', models.CharField(max_length=300, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Proceedings item',
                'verbose_name_plural': 'Proceedings',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='MagazineArticle',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('pages', models.CharField(max_length=25, null=True, blank=True)),
                ('short_title', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Magazine article',
                'verbose_name_plural': 'Magazine articles',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('publisher', models.CharField(max_length=250, null=True, blank=True)),
                ('place', models.CharField(max_length=300, null=True, blank=True)),
                ('volume', models.CharField(max_length=300, null=True, blank=True)),
                ('issn', models.CharField(max_length=100, null=True, verbose_name='ISSN', blank=True)),
                ('issue', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Magazine',
                'verbose_name_plural': 'Magazines',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='JournalArticle',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('pages', models.CharField(max_length=25, null=True, blank=True)),
                ('short_title', models.CharField(max_length=150, null=True, blank=True)),
                ('individually_published', models.DateField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Journal article',
                'verbose_name_plural': 'Journal articles',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('publisher', models.CharField(max_length=250, null=True, blank=True)),
                ('place', models.CharField(max_length=300, null=True, blank=True)),
                ('volume', models.CharField(max_length=300, null=True, blank=True)),
                ('issn', models.CharField(max_length=100, null=True, verbose_name='ISSN', blank=True)),
                ('issue', models.CharField(max_length=150, null=True, blank=True)),
                ('journal_abbreviation', models.CharField(max_length=150, null=True, blank=True)),
                ('quartile', models.CharField(default=None, max_length=25, null=True, blank=True, choices=[(b'Q1', b'Q1'), (b'Q2', b'Q2'), (b'Q3', b'Q3'), (b'Q4', b'Q4'), (None, b'None')])),
                ('impact_factor', models.DecimalField(null=True, max_digits=7, decimal_places=5, blank=True)),
            ],
            options={
                'verbose_name': 'Journal',
                'verbose_name_plural': 'Journals',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='ConferencePaper',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('pages', models.CharField(max_length=25, null=True, blank=True)),
                ('short_title', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Conference paper',
                'verbose_name_plural': 'Conference papers',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='BookSection',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('pages', models.CharField(max_length=25, null=True, blank=True)),
                ('short_title', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Book section',
                'verbose_name_plural': 'Book sections',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('publisher', models.CharField(max_length=250, null=True, blank=True)),
                ('place', models.CharField(max_length=300, null=True, blank=True)),
                ('volume', models.CharField(max_length=300, null=True, blank=True)),
                ('isbn', models.CharField(max_length=100, null=True, verbose_name='ISBN', blank=True)),
                ('edition', models.CharField(max_length=50, null=True, blank=True)),
                ('series', models.CharField(max_length=300, null=True, blank=True)),
                ('series_number', models.PositiveIntegerField(null=True, blank=True)),
                ('number_of_pages', models.PositiveIntegerField(null=True, blank=True)),
                ('number_of_volumes', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='ThesisSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('thesis', models.ForeignKey(to='publications.Thesis')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VivaPanel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=150, choices=[(b'Chair', b'Chair'), (b'Secretary', b'Secretary'), (b'Co-chair', b'Co-chair'), (b'First co-chair', b'First co-chair'), (b'Second co-chair', b'Second co-chair'), (b'Third co-chair', b'Third co-chair'), (b'Vocal', b'Vocal')])),
                ('person', models.ForeignKey(to='persons.Person')),
                ('thesis', models.ForeignKey(to='publications.Thesis')),
            ],
            options={
                'verbose_name': 'VIVA panel',
                'verbose_name_plural': 'VIVA panels',
            },
            bases=(models.Model,),
        ),
    ]
