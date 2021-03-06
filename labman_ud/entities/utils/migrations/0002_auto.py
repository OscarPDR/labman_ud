# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto'),
        ('publications', '0002_auto'),
        ('persons', '__first__'),
        ('utils', '0001_initial'),
        ('events', '__first__'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhDProgram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('homepage', models.URLField(max_length=250)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('faculty', models.ForeignKey(related_name='faculty_holding_a_phd_program', blank=True, to='organizations.Organization')),
                ('university', models.ForeignKey(related_name='university_holding_a_phd_program', to='organizations.Organization')),
            ],
            options={
                'verbose_name': 'PhD program',
                'verbose_name_plural': 'PhD programs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=250)),
                ('short_name', models.CharField(max_length=250, null=True, blank=True)),
                ('slug', models.SlugField(max_length=250, null=True, blank=True)),
                ('description', redactor.fields.RedactorField()),
                ('date', models.DateField(null=True, blank=True)),
                ('event', models.ForeignKey(blank=True, to='events.Event', null=True)),
                ('supporting_organization', models.ForeignKey(blank=True, to='organizations.Organization', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonRelatedToTalkOrCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.ForeignKey(to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TalkOrCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, null=True, blank=True)),
                ('description', redactor.fields.RedactorField()),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('event', models.ForeignKey(blank=True, to='events.Event', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AwardSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('award', models.ForeignKey(to='utils.Award')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CitySeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('city', models.ForeignKey(to='utils.City')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContributionSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('contribution', models.ForeignKey(to='utils.Contribution')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountrySeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('country', models.ForeignKey(to='utils.Country')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileItemRelatedToContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contribution', models.ForeignKey(to='utils.Contribution')),
                ('file_item', models.ForeignKey(to='utils.FileItem')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileItemRelatedToTalkOrCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_item', models.ForeignKey(to='utils.FileItem')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeographicalScopeSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('geographical_scope', models.ForeignKey(to='utils.GeographicalScope')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LanguageSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('language', models.ForeignKey(to='utils.Language')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LicenseSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('license', models.ForeignKey(to='utils.License')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NetworkSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('network', models.ForeignKey(to='utils.Network')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonRelatedToAward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('award', models.ForeignKey(to='utils.Award')),
                ('person', models.ForeignKey(to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonRelatedToContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contribution', models.ForeignKey(to='utils.Contribution')),
                ('person', models.ForeignKey(to='persons.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhDProgramSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('phd_program', models.ForeignKey(to='utils.PhDProgram')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectRelatedToAward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('award', models.ForeignKey(to='utils.Award')),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectRelatedToContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contribution', models.ForeignKey(to='utils.Contribution')),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationRelatedToAward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('award', models.ForeignKey(to='utils.Award')),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationRelatedToContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contribution', models.ForeignKey(to='utils.Contribution')),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('slug', models.SlugField(unique=True, max_length=75, blank=True)),
                ('sub_tag_of', models.ForeignKey(blank=True, to='utils.Tag', null=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagRelatedToContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contribution', models.ForeignKey(to='utils.Contribution')),
                ('tag', models.ForeignKey(to='utils.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagRelatedToTalkOrCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.ForeignKey(to='utils.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('tag', models.ForeignKey(to='utils.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TalkOrCourseSeeAlso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('see_also', models.URLField(max_length=512)),
                ('talk_or_course', models.ForeignKey(to='utils.TalkOrCourse')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tagrelatedtotalkorcourse',
            name='talk_or_course',
            field=models.ForeignKey(to='utils.TalkOrCourse'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelatedtotalkorcourse',
            name='talk_or_course',
            field=models.ForeignKey(to='utils.TalkOrCourse'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personrelatedtotalkorcourse',
            name='talk_or_course',
            field=models.ForeignKey(to='utils.TalkOrCourse'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fileitemrelatedtotalkorcourse',
            name='talk_or_course',
            field=models.ForeignKey(to='utils.TalkOrCourse'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contribution',
            name='contribution_type',
            field=models.ForeignKey(to='utils.ContributionType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contribution',
            name='license',
            field=models.ForeignKey(blank=True, to='utils.License', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(blank=True, to='utils.Country', null=True),
            preserve_default=True,
        ),
    ]
