# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_auto_20141210_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True)),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
            options={
                'verbose_name': 'Publication ranking',
                'verbose_name_plural': 'Publication rankings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_created', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True)),
                ('log_modified', models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=150, choices=[(b'Chair', b'Chair'), (b'Secretary', b'Secretary'), (b'Co-chair', b'Co-chair'), (b'First co-chair', b'First co-chair'), (b'Second co-chair', b'Second co-chair'), (b'Third co-chair', b'Third co-chair'), (b'Vocal', b'Vocal')])),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Ranking',
                'verbose_name_plural': 'Rankings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='publicationrank',
            name='ranking',
            field=models.ForeignKey(to='publications.Ranking'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
        migrations.AlterModelOptions(
            name='booksection',
            options={'verbose_name': 'Book section', 'verbose_name_plural': 'Book sections'},
        ),
        migrations.AlterModelOptions(
            name='coadvisor',
            options={'verbose_name': 'Co-advisor', 'verbose_name_plural': 'Co-advisors'},
        ),
        migrations.AlterModelOptions(
            name='conferencepaper',
            options={'verbose_name': 'Conference paper', 'verbose_name_plural': 'Conference papers'},
        ),
        migrations.AlterModelOptions(
            name='journal',
            options={'verbose_name': 'Journal', 'verbose_name_plural': 'Journals'},
        ),
        migrations.AlterModelOptions(
            name='journalarticle',
            options={'verbose_name': 'Journal article', 'verbose_name_plural': 'Journal articles'},
        ),
        migrations.AlterModelOptions(
            name='magazine',
            options={'verbose_name': 'Magazine', 'verbose_name_plural': 'Magazines'},
        ),
        migrations.AlterModelOptions(
            name='magazinearticle',
            options={'verbose_name': 'Magazine article', 'verbose_name_plural': 'Magazine articles'},
        ),
        migrations.AlterModelOptions(
            name='proceedings',
            options={'verbose_name': 'Proceedings item', 'verbose_name_plural': 'Proceedings'},
        ),
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ['-slug'], 'verbose_name': 'Publication', 'verbose_name_plural': 'Publications'},
        ),
        migrations.AlterModelOptions(
            name='publicationauthor',
            options={'verbose_name': 'Publication author', 'verbose_name_plural': 'Publication authors'},
        ),
        migrations.AlterModelOptions(
            name='publicationeditor',
            options={'verbose_name': 'Publication editor', 'verbose_name_plural': 'Publication editors'},
        ),
        migrations.AlterModelOptions(
            name='thesis',
            options={'ordering': ['slug'], 'verbose_name': 'Thesis', 'verbose_name_plural': 'Theses'},
        ),
        migrations.AlterModelOptions(
            name='thesisabstract',
            options={'verbose_name': 'Thesis abstract', 'verbose_name_plural': 'Thesis abstracts'},
        ),
        migrations.AlterModelOptions(
            name='vivapanel',
            options={'verbose_name': 'VIVA panel', 'verbose_name_plural': 'VIVA panels'},
        ),
        migrations.AddField(
            model_name='publication',
            name='rankings',
            field=models.ManyToManyField(to='publications.Ranking', through='publications.PublicationRank'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coadvisor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coadvisor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationauthor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationauthor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationeditor',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationeditor',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationtag',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationtag',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesis',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesis',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisabstract',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisabstract',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thesisseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vivapanel',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773154), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vivapanel',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 16, 0, 52, 773210), auto_now=True),
            preserve_default=True,
        ),
    ]
