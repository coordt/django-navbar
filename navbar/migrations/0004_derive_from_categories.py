# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.template.defaultfilters import slugify

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Changing field 'NavBarEntry.name'
        db.alter_column('navbar_navbarentry', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Adding field 'NavBarEntry.slug'
        db.add_column('navbar_navbarentry', 'slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, db_index=True), keep_default=False)

        # Adding field 'NavBarEntry.active'
        db.add_column('navbar_navbarentry', 'active', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Changing field 'NavBarEntry.parent'
        db.alter_column('navbar_navbarentry', 'parent_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['navbar.NavBarEntry']))



    def backwards(self, orm):
        
        # Deleting field 'NavBarEntry.slug'
        db.delete_column('navbar_navbarentry', 'slug')

        # Deleting field 'NavBarEntry.active'
        db.delete_column('navbar_navbarentry', 'active')

        # Changing field 'NavBarEntry.parent'
        db.alter_column('navbar_navbarentry', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['navbar.NavBarEntry']))

        # Changing field 'NavBarEntry.name'
        db.alter_column('navbar_navbarentry', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'navbar.navbarentry': {
            'Meta': {'ordering': "('tree_id', 'order')", 'object_name': 'NavBarEntry'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'active_cssclass': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'cssclass': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['navbar.NavBarEntry']"}),
            'path_type': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'})
        }
    }

    complete_apps = ['navbar']
