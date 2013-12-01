from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ucbc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'main.views.index'),
    #url(r'^')
    url(r'^shop/', include('shop.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^flatpages/', include('django.contrib.flatpages.urls')),
)
