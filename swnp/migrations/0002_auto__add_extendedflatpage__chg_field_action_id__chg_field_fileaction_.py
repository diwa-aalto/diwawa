# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExtendedFlatPage'
        db.create_table('swnp_extendedflatpage', (
            ('flatpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['flatpages.FlatPage'], unique=True, primary_key=True)),
            ('show_after', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='flatpage_predecessor', null=True, blank=True, to=orm['swnp.ExtendedFlatPage'])),
            ('alt_text', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('swnp', ['ExtendedFlatPage'])


        # Changing field 'Action.id'
        db.alter_column(u'action', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        # Changing field 'Fileaction.id'
        db.alter_column(u'fileaction', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        # Changing field 'Session.id'
        db.alter_column(u'session', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        # Changing field 'Company.id'
        db.alter_column(u'company', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        # Changing field 'Computer.id'
        db.alter_column(u'computer', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        # Changing field 'File.id'
        db.alter_column(u'file', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        # Changing field 'User.id'
        db.alter_column(u'user', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        # Changing field 'Event.id'
        db.alter_column(u'event', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

        # Changing field 'Project.id'
        db.alter_column(u'project', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

    def backwards(self, orm):
        # Deleting model 'ExtendedFlatPage'
        db.delete_table('swnp_extendedflatpage')


        # Changing field 'Action.id'
        db.alter_column(u'action', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

        # Changing field 'Fileaction.id'
        db.alter_column(u'fileaction', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

        # Changing field 'Session.id'
        db.alter_column(u'session', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

        # Changing field 'Company.id'
        db.alter_column(u'company', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

        # Changing field 'Computer.id'
        db.alter_column(u'computer', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

        # Changing field 'File.id'
        db.alter_column(u'file', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

        # Changing field 'User.id'
        db.alter_column(u'user', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

        # Changing field 'Event.id'
        db.alter_column(u'event', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

        # Changing field 'Project.id'
        db.alter_column(u'project', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'flatpages.flatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'FlatPage', 'db_table': "'django_flatpage'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'swnp.action': {
            'Meta': {'object_name': 'Action', 'db_table': "u'action'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'swnp.computer': {
            'Meta': {'object_name': 'Computer', 'db_table': "u'computer'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Session']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'})
        },
        'swnp.extendedflatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'ExtendedFlatPage', '_ormbases': ['flatpages.FlatPage']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'flatpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['flatpages.FlatPage']", 'unique': 'True', 'primary_key': 'True'}),
            'show_after': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'flatpage_predecessor'", 'null': 'True', 'blank': 'True', 'to': "orm['swnp.ExtendedFlatPage']"})
        },
        'swnp.file': {
            'Meta': {'object_name': 'File', 'db_table': "u'file'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Project']", 'null': 'True', 'blank': 'True'})
        },
        'swnp.fileaction': {
            'Meta': {'object_name': 'Fileaction', 'db_table': "u'fileaction'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Action']"}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Computer']", 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.File']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Session']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.User']", 'null': 'True', 'blank': 'True'})
        },
        'swnp.project': {
            'Meta': {'object_name': 'Project', 'db_table': "u'project'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['swnp.Company']"}),
            'dir': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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