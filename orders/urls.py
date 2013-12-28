from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'orders.views.main'),
    url(r'^grains/$', 'orders.views.grains'),
    url(r'^hops/$', 'orders.views.hops'),
    url(r'^cart/$', 'orders.views.cart'),
    url(r'^cart/delete/$', 'orders.views.cart_delete_item'),
)
