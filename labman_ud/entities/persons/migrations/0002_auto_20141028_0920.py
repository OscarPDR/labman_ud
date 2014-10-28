# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('organizations', '0003_auto_20141028_0920'),
        ('publications', '0001_initial'),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesisregisteredbyperson',
            name='thesis',
            field=models.ForeignKey(to='publications.Thesis'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phdprogramfollowedbyperson',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phdprogramfollowedbyperson',
            name='phd_program',
            field=models.ForeignKey(to='utils.PhDProgram'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personseealso',
            name='person',
            field=models.ForeignKey(related_name=b'see_also_links', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='publications',
            field=models.ManyToManyField(to='publications.Publication', through='publications.PublicationAuthor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nickname',
            name='person',
            field=models.ForeignKey(related_name=b'nicknames', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='organization',
            field=models.ForeignKey(to='organizations.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='network',
            field=models.ForeignKey(to='utils.Network'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
    ]
