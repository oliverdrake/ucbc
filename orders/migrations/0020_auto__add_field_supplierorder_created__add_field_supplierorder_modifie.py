# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SupplierOrder.created'
        db.add_column('orders_supplierorder', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 24, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'SupplierOrder.modified'
        db.add_column('orders_supplierorder', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 24, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'UserOrder.created'
        db.add_column('orders_userorder', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 24, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'UserOrder.modified'
        db.add_column('orders_userorder', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 24, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SupplierOrder.created'
        db.delete_column('orders_supplierorder', 'created')

        # Deleting field 'SupplierOrder.modified'
        db.delete_column('orders_supplierorder', 'modified')

        # Deleting field 'UserOrder.created'
        db.delete_column('orders_userorder', 'created')

        # Deleting field 'UserOrder.modified'
        db.delete_column('orders_userorder', 'modified')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'orders.grain': {
            'Meta': {'object_name': 'Grain', '_ormbases': ['orders.Ingredient']},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['orders.Ingredient']", 'unique': 'True', 'primary_key': 'True'})
        },
        'orders.hop': {
            'Meta': {'object_name': 'Hop', '_ormbases': ['orders.Ingredient']},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['orders.Ingredient']", 'unique': 'True', 'primary_key': 'True'})
        },
        'orders.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ingredients'", 'null': 'True', 'to': "orm['orders.Supplier']"}),
            'unit_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'unit_size': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'orders.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'single_ingredient_orders'", 'to': "orm['orders.Ingredient']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'supplier_order': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ingredient_orders'", 'null': 'True', 'blank': 'True', 'to': "orm['orders.SupplierOrder']"}),
            'user_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_items'", 'to': "orm['orders.UserOrder']"})
        },
        'orders.ordersenabled': {
            'Meta': {'object_name': 'OrdersEnabled'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'orders.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'orders.supplierorder': {
            'Meta': {'object_name': 'SupplierOrder'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '255'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['orders.Supplier']"})
        },
        'orders.userorder': {
            'Meta': {'object_name': 'UserOrder'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'unpaid'", 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['orders']