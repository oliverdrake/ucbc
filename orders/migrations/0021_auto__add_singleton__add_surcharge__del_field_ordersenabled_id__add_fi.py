# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Singleton'
        db.create_table('orders_singleton', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('orders', ['Singleton'])

        # Adding model 'Surcharge'
        db.create_table('orders_surcharge', (
            ('singleton_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['orders.Singleton'], primary_key=True)),
            ('surcharge_percentage', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('orders', ['Surcharge'])

        # Deleting field 'OrdersEnabled.id'
        db.delete_column('orders_ordersenabled', 'id')

        # Adding field 'OrdersEnabled.singleton_ptr'
        db.add_column('orders_ordersenabled', 'singleton_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['orders.Singleton'], default=0, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Singleton'
        db.delete_table('orders_singleton')

        # Deleting model 'Surcharge'
        db.delete_table('orders_surcharge')

        # Adding field 'OrdersEnabled.id'
        db.add_column('orders_ordersenabled', 'id',
                      self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True),
                      keep_default=False)

        # Deleting field 'OrdersEnabled.singleton_ptr'
        db.delete_column('orders_ordersenabled', 'singleton_ptr_id')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
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
            'Meta': {'object_name': 'Grain', '_ormbases': ['orders.Ingredient']},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['orders.Ingredient']", 'primary_key': 'True'})
        },
        'orders.hop': {
            'Meta': {'object_name': 'Hop', '_ormbases': ['orders.Ingredient']},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['orders.Ingredient']", 'primary_key': 'True'})
        },
        'orders.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingredients'", 'null': 'True', 'to': "orm['orders.Supplier']", 'default': 'None'}),
            'unit_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'unit_size': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255'})
        },
        'orders.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'single_ingredient_orders'", 'to': "orm['orders.Ingredient']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'supplier_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingredient_orders'", 'null': 'True', 'to': "orm['orders.SupplierOrder']", 'default': 'None', 'blank': 'True'}),
            'user_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_items'", 'to': "orm['orders.UserOrder']"})
        },
        'orders.ordersenabled': {
            'Meta': {'object_name': 'OrdersEnabled', '_ormbases': ['orders.Singleton']},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'singleton_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['orders.Singleton']", 'primary_key': 'True'})
        },
        'orders.singleton': {
            'Meta': {'object_name': 'Singleton'},
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
        'orders.surcharge': {
            'Meta': {'object_name': 'Surcharge', '_ormbases': ['orders.Singleton']},
            'singleton_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['orders.Singleton']", 'primary_key': 'True'}),
            'surcharge_percentage': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'})
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