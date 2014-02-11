import random
import string
from django.conf.urls import patterns, url, include
from orders.forms import SupplierOrderSupplierForm, SupplierOrderOrderItemsForm

import orders.views as views

RANDOM_PAYPAL_URI = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))

urlpatterns = patterns('',
    url(r'^$', 'orders.views.main'),
    url(r'^grains/$', views.Grains.as_view(), name='order_grain'),
    url(r'^hops/$', views.Hops.as_view(), name='order_hops'),
    url(r'^cart/review/$', 'orders.views.review_order', name='review_order'),
    url(r'^cart/delete/$', 'orders.views.cart_delete_item', name='remove_item'),
    url(r'^cart/$', 'orders.views.checkout', name='checkout'),
    url(r'^complete/(?P<order_id>\d+)/$', 'orders.views.order_complete', name='order_complete'),
    url(r'^history/$', views.UserOrderListView.as_view(), name='order_history'),
    url(r'^order/(?P<order_id>\d+)/$', views.UserOrderItemListView.as_view(), name='order'),
    url(r'^supplier/csv/(?P<order_id>\d+)/$', 'orders.views.supplier_order_summary_csv', name='supplier_order_summary_csv'),
    url(r'^import/(?P<model_name>\w+)/$', 'orders.views.import_ingredients_from_csv', name='import_ingredients'),
    url(r'^payment/(?P<order_id>\d+)/$', 'orders.views.payment', name='payment'),
    url(r'^payment/ASD45623SDF7878aetrty/', include('paypal.standard.ipn.urls')),
)
