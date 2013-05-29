# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectType'
        db.create_table('projects_projecttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1500, blank=True)),
        ))
        db.send_create_signal('projects', ['ProjectType'])

        # Adding model 'Project'
        db.create_table('projects_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_leader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.Organization'])),
            ('project_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectType'])),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=3000)),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=150, null=True, blank=True)),
            ('start_month', self.gf('django.db.models.fields.CharField')(default='01', max_length=25, blank=True)),
            ('start_year', self.gf('django.db.models.fields.IntegerField')()),
            ('end_month', self.gf('django.db.models.fields.CharField')(default='12', max_length=25, blank=True)),
            ('end_year', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='Not started', max_length=25)),
            ('observations', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal('projects', ['Project'])

        # Adding model 'ProjectLogo'
        db.create_table('projects_projectlogo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['ProjectLogo'])

        # Adding model 'Funding'
        db.create_table('projects_funding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('funding_program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['funding_programs.FundingProgram'])),
            ('project_code', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('total_funds', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('projects', ['Funding'])

        # Adding model 'FundingAmount'
        db.create_table('projects_fundingamount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('funding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Funding'])),
            ('consortium_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('own_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('projects', ['FundingAmount'])

        # Adding model 'AssignedPerson'
        db.create_table('projects_assignedperson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.Person'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Role'])),
        ))
        db.send_create_signal('projects', ['AssignedPerson'])

        # Adding model 'ConsortiumMember'
        db.create_table('projects_consortiummember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.Organization'])),
        ))
        db.send_create_signal('projects', ['ConsortiumMember'])

        # Adding model 'RelatedPublication'
        db.create_table('projects_relatedpublication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.Publication'])),
        ))
        db.send_create_signal('projects', ['RelatedPublication'])


    def backwards(self, orm):
        # Deleting model 'ProjectType'
        db.delete_table('projects_projecttype')

        # Deleting model 'Project'
        db.delete_table('projects_project')

        # Deleting model 'ProjectLogo'
        db.delete_table('projects_projectlogo')

        # Deleting model 'Funding'
        db.delete_table('projects_funding')

        # Deleting model 'FundingAmount'
        db.delete_table('projects_fundingamount')

        # Deleting model 'AssignedPerson'
        db.delete_table('projects_assignedperson')

        # Deleting model 'ConsortiumMember'
        db.delete_table('projects_consortiummember')

        # Deleting model 'RelatedPublication'
        db.delete_table('projects_relatedpublication')


    models = {
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventType']"}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'})
        },
        'events.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        'funding_programs.fundingprogram': {
            'Meta': {'object_name': 'FundingProgram'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'geographical_scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.GeographicalScope']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250', 'blank': 'True'})
        },
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Country']"}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.OrganizationType']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'sub_organization_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']", 'null': 'True', 'blank': 'True'})
        },
        'organizations.organizationtype': {
            'Meta': {'object_name': 'OrganizationType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        'persons.person': {
            'Meta': {'object_name': 'Person'},
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_surname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'foaf_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']", 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'second_surname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        'projects.assignedperson': {
            'Meta': {'object_name': 'AssignedPerson'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Person']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Role']"})
        },
        'projects.consortiummember': {
            'Meta': {'object_name': 'ConsortiumMember'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"})
        },
        'projects.funding': {
            'Meta': {'object_name': 'Funding'},
            'funding_program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['funding_programs.FundingProgram']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}),
            'project_code': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'total_funds': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        'projects.fundingamount': {
            'Meta': {'object_name': 'FundingAmount'},
            'consortium_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'funding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Funding']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'own_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'end_month': ('django.db.models.fields.CharField', [], {'default': "'12'", 'max_length': '25', 'blank': 'True'}),
            'end_year': ('django.db.models.fields.IntegerField', [], {}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'project_leader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Organization']"}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ProjectType']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'start_month': ('django.db.models.fields.CharField', [], {'default': "'01'", 'max_length': '25', 'blank': 'True'}),
            'start_year': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Not started'", 'max_length': '25'})
        },
        'projects.projectlogo': {
            'Meta': {'object_name': 'ProjectLogo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"})
        },
        'projects.projecttype': {
            'Meta': {'object_name': 'ProjectType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        'projects.relatedpublication': {
            'Meta': {'object_name': 'RelatedPublication'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Publication']"})
        },
        'publications.publication': {
            'Meta': {'object_name': 'Publication'},
            'abstract': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impact_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'journal_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'presented_at': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']", 'null': 'True', 'blank': 'True'}),
            'proceedings_title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'publication_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.PublicationType']"}),
            'published': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'volume': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'})
        },
        'publications.publicationtype': {
            'Meta': {'object_name': 'PublicationType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'})
        },
        'utils.country': {
            'Meta': {'object_name': 'Country'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250', 'blank': 'True'})
        },
        'utils.geographicalscope': {
            'Meta': {'object_name': 'GeographicalScope'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'})
        },
        'utils.role': {
            'Meta': {'object_name': 'Role'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['projects']