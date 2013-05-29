# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('persons_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_surname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('second_surname', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('foaf_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.Organization'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, blank=True)),
            ('profile_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('persons', ['Person'])

        # Adding model 'Role'
        db.create_table('persons_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1500)),
        ))
        db.send_create_signal('persons', ['Role'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table('persons_person')

        # Deleting model 'Role'
        db.delete_table('persons_role')


    models = {
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
        'persons.role': {
            'Meta': {'object_name': 'Role'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'utils.country': {
            'Meta': {'object_name': 'Country'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['persons']