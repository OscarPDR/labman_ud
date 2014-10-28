# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('organizations', '0003_auto_20141028_0920'),
        ('publications', '0001_initial'),
        ('events', '0003_auto_20141028_0920'),
        ('persons', '0002_auto_20141028_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesisabstract',
            name='language',
            field=models.ForeignKey(to='utils.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thesisabstract',
            name='thesis',
            field=models.ForeignKey(to='publications.Thesis'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thesis',
            name='advisor',
            field=models.ForeignKey(related_name=b'advised_thesis', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thesis',
            name='author',
            field=models.ForeignKey(related_name=b'has_thesis', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thesis',
            name='co_advisors',
            field=models.ManyToManyField(related_name=b'coadvised_thesis', null=True, through='publications.CoAdvisor', to='persons.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thesis',
            name='held_at_university',
            field=models.ForeignKey(blank=True, to='organizations.Organization', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thesis',
            name='main_language',
            field=models.ForeignKey(to='utils.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thesis',
            name='phd_program',
            field=models.ForeignKey(blank=True, to='utils.PhDProgram', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicationtag',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicationtag',
            name='tag',
            field=models.ForeignKey(to='utils.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicationseealso',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicationeditor',
            name='editor',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicationeditor',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicationauthor',
            name='author',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicationauthor',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='authors',
            field=models.ManyToManyField(related_name=b'authors', through='publications.PublicationAuthor', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='editors',
            field=models.ManyToManyField(related_name=b'editors', through='publications.PublicationEditor', to='persons.Person'),
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
            model_name='conferencepaper',
            name='parent_proceedings',
            field=models.ForeignKey(to='publications.Proceedings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conferencepaper',
            name='presented_at',
            field=models.ForeignKey(blank=True, to='events.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coadvisor',
            name='co_advisor',
            field=models.ForeignKey(to='persons.Person'),
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
