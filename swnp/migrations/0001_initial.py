# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('swnp', ['Company'])

        # Adding model 'User'
        db.create_table(u'user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Company'], null=True, blank=True)),
        ))
        db.send_create_signal('swnp', ['User'])

        # Adding model 'Project'
        db.create_table(u'project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Company'])),
            ('dir', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=120, blank=True)),
        ))
        db.send_create_signal('swnp', ['Project'])

        # Adding model 'Session'
        db.create_table(u'session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Project'])),
            ('starttime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('endtime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('previous_session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Session'], null=True, blank=True)),
        ))
        db.send_create_signal('swnp', ['Session'])

        # Adding model 'Action'
        db.create_table(u'action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal('swnp', ['Action'])

        # Adding model 'Computer'
        db.create_table(u'computer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('ip', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('screens', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.User'], null=True, blank=True)),
            ('wos_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('swnp', ['Computer'])

        # Adding model 'Event'
        db.create_table(u'event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=1500, null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Session'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
        ))
        db.send_create_signal('swnp', ['Event'])

        # Adding model 'File'
        db.create_table(u'file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Project'], null=True, blank=True)),
        ))
        db.send_create_signal('swnp', ['File'])

        # Adding model 'Fileaction'
        db.create_table(u'fileaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.File'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Action'])),
            ('action_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.User'], null=True, blank=True)),
            ('computer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Computer'], null=True, blank=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Session'], null=True, blank=True)),
        ))
        db.send_create_signal('swnp', ['Fileaction'])

        # Adding model 'Projectmembers'
        db.create_table(u'projectmembers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Project'], null=True, db_column='Project', blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.User'], null=True, db_column='User', blank=True)),
        ))
        db.send_create_signal('swnp', ['Projectmembers'])

        # Adding model 'Activity'
        db.create_table(u'activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activities', to=orm['swnp.Project'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='activities', null=True, to=orm['swnp.Session'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('swnp', ['Activity'])

        # Adding model 'Sessioncomputers'
        db.create_table(u'sessioncomputers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Session'], null=True, db_column='Session', blank=True)),
            ('computer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Computer'], null=True, db_column='Computer', blank=True)),
        ))
        db.send_create_signal('swnp', ['Sessioncomputers'])

        # Adding model 'Sessionparticipants'
        db.create_table(u'sessionparticipants', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.Session'], null=True, db_column='Session', blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['swnp.User'], null=True, db_column='User', blank=True)),
        ))
        db.send_create_signal('swnp', ['Sessionparticipants'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table(u'company')

        # Deleting model 'User'
        db.delete_table(u'user')

        # Deleting model 'Project'
        db.delete_table(u'project')

        # Deleting model 'Session'
        db.delete_table(u'session')

        # Deleting model 'Action'
        db.delete_table(u'action')

        # Deleting model 'Computer'
        db.delete_table(u'computer')

        # Deleting model 'Event'
        db.delete_table(u'event')

        # Deleting model 'File'
        db.delete_table(u'file')

        # Deleting model 'Fileaction'
        db.delete_table(u'fileaction')

        # Deleting model 'Projectmembers'
        db.delete_table(u'projectmembers')

        # Deleting model 'Activity'
        db.delete_table(u'activity')

        # Deleting model 'Sessioncomputers'
        db.delete_table(u'sessioncomputers')

        # Deleting model 'Sessionparticipants'
        db.delete_table(u'sessionparticipants')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'swnp.action': {
            'Meta': {'object_name': 'Action', 'db_table': "u'action'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'swnp.activity': {
            'Meta': {'object_name': 'Activity', 'db_table': "u'activity'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': "orm['swnp.Project']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activities'", 'null': 'True', 'to': "orm['swnp.Session']"})
        },
        'swnp.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'swnp.computer': {
            'Meta': {'object_name': 'Computer', 'db_table': "u'computer'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'screens': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.User']", 'null': 'True', 'blank': 'True'}),
            'wos_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'swnp.event': {
            'Meta': {'object_name': 'Event', 'db_table': "u'event'"},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '1500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Session']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'})
        },
        'swnp.file': {
            'Meta': {'object_name': 'File', 'db_table': "u'file'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Project']", 'null': 'True', 'blank': 'True'})
        },
        'swnp.fileaction': {
            'Meta': {'object_name': 'Fileaction', 'db_table': "u'fileaction'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Action']"}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Computer']", 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.File']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Session']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.User']", 'null': 'True', 'blank': 'True'})
        },
        'swnp.project': {
            'Meta': {'object_name': 'Project', 'db_table': "u'project'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Company']"}),
            'dir': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'})
        },
        'swnp.projectmembers': {
            'Meta': {'object_name': 'Projectmembers', 'db_table': "u'projectmembers'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Project']", 'null': 'True', 'db_column': "'Project'", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.User']", 'null': 'True', 'db_column': "'User'", 'blank': 'True'})
        },
        'swnp.session': {
            'Meta': {'object_name': 'Session', 'db_table': "u'session'"},
            'endtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'previous_session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Session']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Project']"}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'swnp.sessioncomputers': {
            'Meta': {'object_name': 'Sessioncomputers', 'db_table': "u'sessioncomputers'"},
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Computer']", 'null': 'True', 'db_column': "'Computer'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Session']", 'null': 'True', 'db_column': "'Session'", 'blank': 'True'})
        },
        'swnp.sessionparticipants': {
            'Meta': {'object_name': 'Sessionparticipants', 'db_table': "u'sessionparticipants'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Session']", 'null': 'True', 'db_column': "'Session'", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.User']", 'null': 'True', 'db_column': "'User'", 'blank': 'True'})
        },
        'swnp.user': {
            'Meta': {'object_name': 'User', 'db_table': "u'user'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Company']", 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['swnp']