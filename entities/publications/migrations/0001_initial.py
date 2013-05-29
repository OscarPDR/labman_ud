# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PublicationType'
        db.create_table('publications_publicationtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1500, blank=True)),
        ))
        db.send_create_signal('publications', ['PublicationType'])

        # Adding model 'Publication'
        db.create_table('publications_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('presented_at', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'], null=True, blank=True)),
            ('publication_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.PublicationType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('proceedings_title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=250, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(max_length=5000, blank=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('journal_abbreviation', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('impact_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=8, blank=True)),
            ('observations', self.gf('django.db.models.fields.TextField')(max_length=3000, blank=True)),
        ))
        db.send_create_signal('publications', ['Publication'])

        # Adding model 'PublicationTag'
        db.create_table('publications_publicationtag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Tag'])),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.Publication'])),
        ))
        db.send_create_signal('publications', ['PublicationTag'])

        # Adding model 'PublicationAuthor'
        db.create_table('publications_publicationauthor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.Person'])),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.Publication'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('publications', ['PublicationAuthor'])


    def backwards(self, orm):
        # Deleting model 'PublicationType'
        db.delete_table('publications_publicationtype')

        # Deleting model 'Publication'
        db.delete_table('publications_publication')

        # Deleting model 'PublicationTag'
        db.delete_table('publications_publicationtag')

        # Deleting model 'PublicationAuthor'
        db.delete_table('publications_publicationauthor')


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
        'publications.publicationauthor': {
            'Meta': {'object_name': 'PublicationAuthor'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Person']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Publication']"})
        },
        'publications.publicationtag': {
            'Meta': {'object_name': 'PublicationTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Publication']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Tag']"})
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
        'utils.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['publications']