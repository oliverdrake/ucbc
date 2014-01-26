# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Singleton'
        db.delete_table('orders_singleton')

        # Deleting field 'OrdersEnabled.singleton_ptr'
        db.delete_column('orders_ordersenabled', 'singleton_ptr_id')

        # Adding field 'OrdersEnabled.id'
        db.add_column('orders_ordersenabled', 'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True, default=1),
                      keep_default=False)

        # Deleting field 'Surcharge.singleton_ptr'
        db.delete_column('orders_surcharge', 'singleton_ptr_id')

        # Adding field 'Surcharge.id'
        db.add_column('orders_surcharge', 'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True, default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Singleton'
        db.create_table('orders_singleton', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('orders', ['Singleton'])

        # Adding field 'OrdersEnabled.singleton_ptr'
        db.add_column('orders_ordersenabled', 'singleton_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, default=0, to=orm['orders.Singleton']),
                      keep_default=False)

        # Deleting field 'OrdersEnabled.id'
        db.delete_column('orders_ordersenabled', 'id')

        # Adding field 'Surcharge.singleton_ptr'
        db.add_column('orders_surcharge', 'singleton_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, default=0, to=orm['orders.Singleton']),
                      keep_default=False)

        # Deleting field 'Surcharge.id'
        db.delete_column('orders_surcharge', 'id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'orders.grain': {
            'Meta': {'_ormbases': ['orders.Ingredient'], 'object_name': 'Grain'},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['orders.Ingredient']"})
        },
        'orders.hop': {
            'Meta': {'_ormbases': ['orders.Ingredient'], 'object_name': 'Hop'},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['orders.Ingredient']"})
        },
        'orders.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingredients'", 'null': 'True', 'default': 'None', 'to': "orm['orders.Supplier']"}),
            'unit_cost': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'unit_size': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'orders.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'single_ingredient_orders'", 'to': "orm['orders.Ingredient']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'supplier_order': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ingredient_orders'", 'null': 'True', 'default': 'None', 'to': "orm['orders.SupplierOrder']"}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'pending'"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['orders.Supplier']"})
        },
        'orders.surcharge': {
            'Meta': {'object_name': 'Surcharge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'surcharge_percentage': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5', 'default': '0.0'})
        },
        'orders.userorder': {
            'Meta': {'object_name': 'UserOrder'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'unpaid'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['orders']