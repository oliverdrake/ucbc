# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field supplier_order on 'SingleIngredientOrder'
        db.delete_table(db.shorten_name('orders_singleingredientorder_supplier_order'))

        # Adding M2M table for field single_ingredient_orders on 'SupplierOrder'
        m2m_table_name = db.shorten_name('orders_supplierorder_single_ingredient_orders')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('supplierorder', models.ForeignKey(orm['orders.supplierorder'], null=False)),
            ('singleingredientorder', models.ForeignKey(orm['orders.singleingredientorder'], null=False))
        ))
        db.create_unique(m2m_table_name, ['supplierorder_id', 'singleingredientorder_id'])


    def backwards(self, orm):
        # Adding M2M table for field supplier_order on 'SingleIngredientOrder'
        m2m_table_name = db.shorten_name('orders_singleingredientorder_supplier_order')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('singleingredientorder', models.ForeignKey(orm['orders.singleingredientorder'], null=False)),
            ('supplierorder', models.ForeignKey(orm['orders.supplierorder'], null=False))
        ))
        db.create_unique(m2m_table_name, ['singleingredientorder_id', 'supplierorder_id'])

        # Removing M2M table for field single_ingredient_orders on 'SupplierOrder'
        db.delete_table(db.shorten_name('orders_supplierorder_single_ingredient_orders'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'orders.grain': {
            'Meta': {'_ormbases': ['orders.Ingredient'], 'object_name': 'Grain'},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['orders.Ingredient']", 'unique': 'True'})
        },
        'orders.hop': {
            'Meta': {'_ormbases': ['orders.Ingredient'], 'object_name': 'Hop'},
            'ingredient_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['orders.Ingredient']", 'unique': 'True'})
        },
        'orders.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['orders.Supplier']", 'null': 'True', 'related_name': "'ingredients'"}),
            'unit_cost': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'unit_size': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'orders.singleingredientorder': {
            'Meta': {'object_name': 'SingleIngredientOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Ingredient']", 'related_name': "'single_ingredient_orders'"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.UserOrder']", 'related_name': "'ingredient_orders'"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'orders.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'orders.supplierorder': {
            'Meta': {'object_name': 'SupplierOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'single_ingredient_orders': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['orders.SingleIngredientOrder']", 'null': 'True', 'related_name': "'supplier_orders'"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '255'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Supplier']", 'related_name': "'orders'"})
        },
        'orders.userorder': {
            'Meta': {'object_name': 'UserOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'orders'"})
        }
    }

    complete_apps = ['orders']