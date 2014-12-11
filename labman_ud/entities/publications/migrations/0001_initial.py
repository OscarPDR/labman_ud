# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import datetime
import django.core.validators
import entities.publications.models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '__first__'),
        ('events', '__first__'),
        ('persons', '__first__'),
        ('organizations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoAdvisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('co_advisor', models.ForeignKey(to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('abstract', models.TextField(max_length=2500, null=True, blank=True)),
                ('doi', models.CharField(max_length=100, null=True, verbose_name='DOI', blank=True)),
                ('published', models.DateField(null=True, blank=True)),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1950), django.core.validators.MaxValueValidator(2080)])),
                ('pdf', models.FileField(max_length=1000, null=True, upload_to=entities.publications.models.publication_path, blank=True)),
                ('bibtex', models.TextField(max_length=2500, null=True, blank=True)),
                ('child_type', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'ordering': ['-slug'],
            },
            bases=(models.Model,),
        ),
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
                'abstract': False,
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
                'abstract': False,
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
                'abstract': False,
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='JournalArticle',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('pages', models.CharField(max_length=25, null=True, blank=True)),
                ('short_title', models.CharField(max_length=150, null=True, blank=True)),
                ('isi', models.BooleanField(default=False, verbose_name='ISI')),
                ('dblp', models.BooleanField(default=False, verbose_name='DBLP')),
                ('individually_published', models.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
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
                'abstract': False,
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='ConferencePaper',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('pages', models.CharField(max_length=25, null=True, blank=True)),
                ('short_title', models.CharField(max_length=150, null=True, blank=True)),
                ('isi', models.BooleanField(default=False, verbose_name='ISI')),
                ('dblp', models.BooleanField(default=False, verbose_name='DBLP')),
                ('core', models.CharField(blank=True, max_length=25, null=True, choices=[(b'A', b'Core A'), (b'B', b'Core B'), (b'C', b'Core C'), (None, b'None')])),
                ('parent_proceedings', models.ForeignKey(to='publications.Proceedings')),
                ('presented_at', models.ForeignKey(blank=True, to='events.Event', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='BookSection',
            fields=[
                ('publication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='publications.Publication')),
                ('pages', models.CharField(max_length=25, null=True, blank=True)),
                ('short_title', models.CharField(max_length=150, null=True, blank=True)),
                ('isi', models.BooleanField(default=False, verbose_name='ISI')),
                ('dblp', models.BooleanField(default=False, verbose_name='DBLP')),
                ('core', models.CharField(blank=True, max_length=25, null=True, choices=[(b'A', b'Core A'), (b'B', b'Core B'), (b'C', b'Core C'), (None, b'None')])),
            ],
            options={
                'abstract': False,
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
                'abstract': False,
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='PublicationAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True)),
                ('author', models.ForeignKey(to='persons.Person')),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationEditor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('editor', models.ForeignKey(to='persons.Person')),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('see_also', models.URLField(max_length=512)),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('publication', models.ForeignKey(to='publications.Publication')),
                ('tag', models.ForeignKey(to='utils.Tag')),
            ],
            options={
                'ordering': ['tag__slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('title', models.CharField(max_length=1000)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('registration_date', models.DateField(null=True, blank=True)),
                ('year', models.PositiveIntegerField()),
                ('pdf', models.FileField(null=True, upload_to=entities.publications.models.thesis_path, blank=True)),
                ('number_of_pages', models.PositiveIntegerField(null=True, blank=True)),
                ('viva_date', models.DateTimeField()),
                ('viva_outcome', models.CharField(default=b'Apt', max_length=250, blank=True, choices=[(b'Apt', b'Apt'), (b'Cum Laude', b'Cum Laude'), (b'Cum Laude by unanimity', b'Cum Laude by unanimity')])),
                ('advisor', models.ForeignKey(related_name='advised_thesis', to='persons.Person')),
                ('author', models.ForeignKey(related_name='has_thesis', to='persons.Person')),
                ('co_advisors', models.ManyToManyField(related_name='coadvised_thesis', null=True, through='publications.CoAdvisor', to='persons.Person', blank=True)),
                ('held_at_university', models.ForeignKey(blank=True, to='organizations.Organization', null=True)),
                ('main_language', models.ForeignKey(to='utils.Language')),
                ('phd_program', models.ForeignKey(blank=True, to='utils.PhDProgram', null=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThesisAbstract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('abstract', redactor.fields.RedactorField(max_length=5000, blank=True)),
                ('language', models.ForeignKey(to='utils.Language')),
                ('thesis', models.ForeignKey(to='publications.Thesis')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThesisSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
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
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248312), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 11, 57, 48, 248370), auto_now=True)),
                ('role', models.CharField(max_length=150, choices=[(b'Chair', b'Chair'), (b'Secretary', b'Secretary'), (b'Co-chair', b'Co-chair'), (b'First co-chair', b'First co-chair'), (b'Second co-chair', b'Second co-chair'), (b'Third co-chair', b'Third co-chair'), (b'Vocal', b'Vocal')])),
                ('person', models.ForeignKey(to='persons.Person')),
                ('thesis', models.ForeignKey(to='publications.Thesis')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='publication',
            name='authors',
            field=models.ManyToManyField(related_name='authors', through='publications.PublicationAuthor', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='editors',
            field=models.ManyToManyField(related_name='editors', through='publications.PublicationEditor', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='language',
            field=models.ForeignKey(blank=True, to='utils.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='tags',
            field=models.ManyToManyField(to='utils.Tag', through='publications.PublicationTag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='magazinearticle',
            name='parent_magazine',
            field=models.ForeignKey(to='publications.Magazine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journalarticle',
            name='parent_journal',
            field=models.ForeignKey(to='publications.Journal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coadvisor',
            name='thesis',
            field=models.ForeignKey(to='publications.Thesis'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booksection',
            name='parent_book',
            field=models.ForeignKey(to='publications.Book'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booksection',
            name='presented_at',
            field=models.ForeignKey(blank=True, to='events.Event', null=True),
            preserve_default=True,
        ),
    ]
