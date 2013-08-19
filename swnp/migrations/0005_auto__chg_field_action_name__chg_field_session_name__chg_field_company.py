# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Action.name'
        db.alter_column(u'action', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Session.name'
        db.alter_column(u'session', 'name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Company.name'
        db.alter_column(u'company', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Adding field 'Computer.pgm_group'
        db.add_column(u'computer', 'pgm_group',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)


        # Changing field 'Computer.name'
        db.alter_column(u'computer', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Computer.mac'
        db.alter_column(u'computer', 'mac', self.gf('django.db.models.fields.CharField')(max_length=12, null=True))

        # Changing field 'Computer.responsive'
        db.alter_column(u'computer', 'responsive', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'File.path'
        db.alter_column(u'file', 'path', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'User.name'
        db.alter_column(u'user', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'User.title'
        db.alter_column(u'user', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'User.email'
        db.alter_column(u'user', 'email', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'User.department'
        db.alter_column(u'user', 'department', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Event.desc'
        db.alter_column(u'event', 'desc', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))

        # Changing field 'Event.title'
        db.alter_column(u'event', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=40))

        # Changing field 'Project.password'
        db.alter_column(u'project', 'password', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

        # Changing field 'Project.dir'
        db.alter_column(u'project', 'dir', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Project.name'
        db.alter_column(u'project', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'Action.name'
        db.alter_column(u'action', 'name', self.gf('django.db.models.fields.CharField')(max_length=150))

        # Changing field 'Session.name'
        db.alter_column(u'session', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=150))

        # Changing field 'Company.name'
        db.alter_column(u'company', 'name', self.gf('django.db.models.fields.CharField')(max_length=150))
        # Deleting field 'Computer.pgm_group'
        db.delete_column(u'computer', 'pgm_group')


        # Changing field 'Computer.name'
        db.alter_column(u'computer', 'name', self.gf('django.db.models.fields.CharField')(max_length=150))

        # Changing field 'Computer.mac'
        db.alter_column(u'computer', 'mac', self.gf('django.db.models.fields.CharField')(default='', max_length=36))

        # Changing field 'Computer.responsive'
        db.alter_column(u'computer', 'responsive', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'File.path'
        db.alter_column(u'file', 'path', self.gf('django.db.models.fields.CharField')(max_length=765))

        # Changing field 'User.name'
        db.alter_column(u'user', 'name', self.gf('django.db.models.fields.CharField')(max_length=150))

        # Changing field 'User.title'
        db.alter_column(u'user', 'title', self.gf('django.db.models.fields.CharField')(max_length=150))

        # Changing field 'User.email'
        db.alter_column(u'user', 'email', self.gf('django.db.models.fields.CharField')(max_length=300))

        # Changing field 'User.department'
        db.alter_column(u'user', 'department', self.gf('django.db.models.fields.CharField')(max_length=300))

        # Changing field 'Event.desc'
        db.alter_column(u'event', 'desc', self.gf('django.db.models.fields.CharField')(max_length=1500, null=True))

        # Changing field 'Event.title'
        db.alter_column(u'event', 'title', self.gf('django.db.models.fields.CharField')(max_length=120, null=True))

        # Changing field 'Project.password'
        db.alter_column(u'project', 'password', self.gf('django.db.models.fields.CharField')(default='', max_length=120))

        # Changing field 'Project.dir'
        db.alter_column(u'project', 'dir', self.gf('django.db.models.fields.CharField')(default='', max_length=765))

        # Changing field 'Project.name'
        db.alter_column(u'project', 'name', self.gf('django.db.models.fields.CharField')(max_length=150))

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flatpages.flatpage': {
            'Meta': {'ordering': "(u'url',)", 'object_name': 'FlatPage', 'db_table': "u'django_flatpage'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'swnp.action': {
            'Meta': {'object_name': 'Action', 'db_table': "u'action'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'swnp.activity': {
            'Meta': {'object_name': 'Activity', 'db_table': "u'activity'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': u"orm['swnp.Project']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activities'", 'null': 'True', 'to': u"orm['swnp.Session']"})
        },
        u'swnp.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'swnp.computer': {
            'Meta': {'object_name': 'Computer', 'db_table': "u'computer'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pgm_group': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'responsive': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'screens': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.User']", 'null': 'True', 'blank': 'True'}),
            'wos_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'swnp.event': {
            'Meta': {'object_name': 'Event', 'db_table': "u'event'"},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Session']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'swnp.extendedflatpage': {
            'Meta': {'ordering': "(u'url',)", 'object_name': 'ExtendedFlatPage', '_ormbases': [u'flatpages.FlatPage']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'flatpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['flatpages.FlatPage']", 'unique': 'True', 'primary_key': 'True'}),
            'show_after': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'flatpage_predecessor'", 'null': 'True', 'blank': 'True', 'to': u"orm['swnp.ExtendedFlatPage']"})
        },
        u'swnp.file': {
            'Meta': {'object_name': 'File', 'db_table': "u'file'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Project']", 'null': 'True', 'blank': 'True'})
        },
        u'swnp.fileaction': {
            'Meta': {'object_name': 'Fileaction', 'db_table': "u'fileaction'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Action']"}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Computer']", 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Session']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.User']", 'null': 'True', 'blank': 'True'})
        },
        u'swnp.project': {
            'Meta': {'object_name': 'Project', 'db_table': "u'project'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Company']"}),
            'dir': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'swnp.projectmembers': {
            'Meta': {'object_name': 'Projectmembers', 'db_table': "u'projectmembers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Project']", 'null': 'True', 'db_column': "'Project'", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.User']", 'null': 'True', 'db_column': "'User'", 'blank': 'True'})
        },
        u'swnp.session': {
            'Meta': {'object_name': 'Session', 'db_table': "u'session'"},
            'endtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'previous_session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Session']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Project']"}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'swnp.sessioncomputers': {
            'Meta': {'object_name': 'Sessioncomputers', 'db_table': "u'sessioncomputers'"},
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Computer']", 'null': 'True', 'db_column': "'Computer'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Session']", 'null': 'True', 'db_column': "'Session'", 'blank': 'True'})
        },
        u'swnp.sessionparticipants': {
            'Meta': {'object_name': 'Sessionparticipants', 'db_table': "u'sessionparticipants'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Session']", 'null': 'True', 'db_column': "'Session'", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.User']", 'null': 'True', 'db_column': "'User'", 'blank': 'True'})
        },
        u'swnp.user': {
            'Meta': {'object_name': 'User', 'db_table': "u'user'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['swnp.Company']", 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['swnp']