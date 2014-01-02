from django.conf.urls import patterns, url

import orders.views as views

urlpatterns = patterns('',
    url(r'^$', 'orders.views.main'),
    url(r'^grains/$', views.Grains.as_view(), name='order_grain'),
    url(r'^hops/$', views.Hops.as_view(), name='order_hops'),
    url(r'^cart/$', 'orders.views.checkout', name='checkout'),
    url(r'^cart/delete/$', 'orders.views.cart_delete_item', name='remove_item'),
    # url(r'^checkout/$', 'orders.views.checkout', name='checkout'),
    url(r'^complete/$', 'orders.views.order_complete', name='order_complete'),
)
