# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntryCategory'
        db.create_table('frequently_entrycategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('frequently', ['EntryCategory'])

        # Adding model 'Entry'
        db.create_table('frequently_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 28, 0, 0))),
            ('last_view_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 28, 0, 0))),
            ('amount_of_views', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('frequently', ['Entry'])

        # Adding M2M table for field category on 'Entry'
        db.create_table('frequently_entry_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['frequently.entry'], null=False)),
            ('entrycategory', models.ForeignKey(orm['frequently.entrycategory'], null=False))
        ))
        db.create_unique('frequently_entry_category', ['entry_id', 'entrycategory_id'])

        # Adding model 'Feedback'
        db.create_table('frequently_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frequently.Entry'], blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')()),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 28, 0, 0))),
            ('validation', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('frequently', ['Feedback'])


    def backwards(self, orm):
        # Deleting model 'EntryCategory'
        db.delete_table('frequently_entrycategory')

        # Deleting model 'Entry'
        db.delete_table('frequently_entry')

        # Removing M2M table for field category on 'Entry'
        db.delete_table('frequently_entry_category')

        # Deleting model 'Feedback'
        db.delete_table('frequently_feedback')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'frequently.entry': {
            'Meta': {'ordering': "['amount_of_views']", 'object_name': 'Entry'},
            'amount_of_views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories'", 'symmetrical': 'False', 'to': "orm['frequently.EntryCategory']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 28, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_view_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 28, 0, 0)'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'frequently.entrycategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'EntryCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'frequently.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frequently.Entry']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remark': ('django.db.models.fields.TextField', [], {}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 28, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'validation': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['frequently']