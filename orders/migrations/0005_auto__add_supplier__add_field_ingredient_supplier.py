# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Supplier'
        db.create_table('orders_supplier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('orders', ['Supplier'])

        # Adding field 'Ingredient.supplier'
        db.add_column('orders_ingredient', 'supplier',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='ingredients', default=None, to=orm['orders.Supplier'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Supplier'
        db.delete_table('orders_supplier')

        # Deleting field 'Ingredient.supplier'
        db.delete_column('orders_ingredient', 'supplier_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'orders.grain': {
            'Meta': {'object_name': 'Grain', '_ormbases': ['orders.Ingredient']},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['orders.Ingredient']"})
        },
        'orders.hop': {
            'Meta': {'object_name': 'Hop', '_ormbases': ['orders.Ingredient']},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['orders.Ingredient']"})
        },
        'orders.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingredients'", 'default': 'None', 'to': "orm['orders.Supplier']", 'null': 'True'}),
            'unit_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'orders.order': {
            'Meta': {'object_name': 'Order'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['auth.User']"})
        },
        'orders.singleingredientorder': {
            'Meta': {'object_name': 'SingleIngredientOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'single_ingredient_orders'", 'to': "orm['orders.Ingredient']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingredient_orders'", 'to': "orm['orders.Order']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'orders.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['orders']