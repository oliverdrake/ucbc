# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SingleIngredientOrder'
        db.delete_table('orders_singleingredientorder')

        # Adding model 'OrderItem'
        db.create_table('orders_orderitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Ingredient'], related_name='single_ingredient_orders')),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.UserOrder'], related_name='ingredient_orders')),
            ('supplier_order', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['orders.SupplierOrder'], related_name='ingredient_orders', default=None)),
        ))
        db.send_create_signal('orders', ['OrderItem'])


    def backwards(self, orm):
        # Adding model 'SingleIngredientOrder'
        db.create_table('orders_singleingredientorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier_order', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['orders.SupplierOrder'], related_name='ingredient_orders', default=None)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Ingredient'], related_name='single_ingredient_orders')),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.UserOrder'], related_name='ingredient_orders')),
        ))
        db.send_create_signal('orders', ['SingleIngredientOrder'])

        # Deleting model 'OrderItem'
        db.delete_table('orders_orderitem')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'orders.grain': {
            'Meta': {'_ormbases': ['orders.Ingredient'], 'object_name': 'Grain'},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['orders.Ingredient']", 'unique': 'True', 'primary_key': 'True'})
        },
        'orders.hop': {
            'Meta': {'_ormbases': ['orders.Ingredient'], 'object_name': 'Hop'},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['orders.Ingredient']", 'unique': 'True', 'primary_key': 'True'})
        },
        'orders.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['orders.Supplier']", 'related_name': "'ingredients'", 'default': 'None'}),
            'unit_cost': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'unit_size': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255'})
        },
        'orders.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Ingredient']", 'related_name': "'single_ingredient_orders'"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.UserOrder']", 'related_name': "'ingredient_orders'"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'supplier_order': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['orders.SupplierOrder']", 'related_name': "'ingredient_orders'", 'default': 'None'})
        },
        'orders.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'orders.supplierorder': {
            'Meta': {'object_name': 'SupplierOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'pending'"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Supplier']", 'related_name': "'orders'"})
        },
        'orders.userorder': {
            'Meta': {'object_name': 'UserOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'pending'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'orders'"})
        }
    }

    complete_apps = ['orders']