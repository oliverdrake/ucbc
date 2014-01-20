from django.conf.urls import patterns, url
from orders.forms import SupplierOrderSupplierForm, SupplierOrderOrderItemsForm

import orders.views as views

supplier_order_wizard = views.SupplierOrderWizard.as_view([SupplierOrderSupplierForm, SupplierOrderOrderItemsForm])
urlpatterns = patterns('',
    url(r'^$', 'orders.views.main'),
    url(r'^grains/$', views.Grains.as_view(), name='order_grain'),
    url(r'^hops/$', views.Hops.as_view(), name='order_hops'),
    url(r'^cart/review/$', 'orders.views.review_order', name='review_order'),
    url(r'^cart/delete/$', 'orders.views.cart_delete_item', name='remove_item'),
    url(r'^cart/$', 'orders.views.checkout', name='checkout'),
    url(r'^complete/(?P<order_id>\d+)/$', 'orders.views.order_complete', name='order_complete'),
    url(r'^supplier/change/$', supplier_order_wizard, name='change_supplier_orders'),
    url(r'^supplier/(?P<order_id>\d+)/$', 'orders.views.supplier_order', name='supplier_order'),
    url(r'^supplier/all/$', views.SupplierOrderList.as_view(), name='supplier_order_list'),
)
