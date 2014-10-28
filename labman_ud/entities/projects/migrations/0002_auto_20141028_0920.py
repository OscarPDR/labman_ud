# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('persons', '0002_auto_20141028_0920'),
        ('publications', '0001_initial'),
        ('projects', '0001_initial'),
        ('funding_programs', '0002_auto_20141028_0920'),
        ('organizations', '0003_auto_20141028_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatedpublication',
            name='publication',
            field=models.ForeignKey(related_name=b'projects', to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttag',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttag',
            name='tag',
            field=models.ForeignKey(to='utils.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectseealso',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='assigned_people',
            field=models.ManyToManyField(related_name=b'projects', through='projects.AssignedPerson', to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='consortium_members',
            field=models.ManyToManyField(related_name=b'consortium_member_of', through='projects.ConsortiumMember', to='organizations.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='project_leader',
            field=models.ForeignKey(to='organizations.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='related_publications',
            field=models.ManyToManyField(related_name=b'related_projects', through='projects.RelatedPublication', to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(related_name=b'projects', through='projects.ProjectTag', to='utils.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fundingseealso',
            name='funding',
            field=models.ForeignKey(to='projects.Funding'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fundingamount',
            name='funding',
            field=models.ForeignKey(to='projects.Funding'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='funding',
            name='funding_program',
            field=models.ForeignKey(to='funding_programs.FundingProgram'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='funding',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consortiummember',
            name='organization',
            field=models.ForeignKey(to='organizations.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consortiummember',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedpersontag',
            name='assigned_person',
            field=models.ForeignKey(to='projects.AssignedPerson'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedpersontag',
            name='tag',
            field=models.ForeignKey(to='utils.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedperson',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedperson',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedperson',
            name='role',
            field=models.ForeignKey(to='utils.Role'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedperson',
            name='tags',
            field=models.ManyToManyField(related_name=b'assigned_persons', through='projects.AssignedPersonTag', to='utils.Tag'),
            preserve_default=True,
        ),
    ]
