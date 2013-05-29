# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventType'
        db.create_table('events_eventtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1500, blank=True)),
        ))
        db.send_create_signal('events', ['EventType'])

        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.EventType'])),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1500, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('observations', self.gf('django.db.models.fields.TextField')(max_length=1500, blank=True)),
        ))
        db.send_create_signal('events', ['Event'])

        # Adding model 'EventLogo'
        db.create_table('events_eventlogo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('events', ['EventLogo'])


    def backwards(self, orm):
        # Deleting model 'EventType'
        db.delete_table('events_eventtype')

        # Deleting model 'Event'
        db.delete_table('events_event')

        # Deleting model 'EventLogo'
        db.delete_table('events_eventlogo')


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
        'events.eventlogo': {
            'Meta': {'object_name': 'EventLogo'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'events.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['events']