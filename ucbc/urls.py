from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse

AuthenticationForm.base_fields['username'].widget.attrs['class'] = "form-control input-sm"
AuthenticationForm.base_fields['username'].widget.attrs['placeholder'] = 'Username'
AuthenticationForm.base_fields['password'].widget.attrs['class'] = "form-control input-sm"
AuthenticationForm.base_fields['password'].widget.attrs['placeholder'] = 'Password'


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ucbc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'main.views.index'),
    #url(r'^')
    url(r'^orders/', include('orders.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', kwargs=dict(next_page="/"), name="logout"),

    #url(r'^flatpages/', include('django.contrib.flatpages.urls')),
)
