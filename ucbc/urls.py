from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

AuthenticationForm.base_fields['username'].widget.attrs['class'] = "form-control input-sm"
AuthenticationForm.base_fields['username'].widget.attrs['placeholder'] = 'Username'
AuthenticationForm.base_fields['password'].widget.attrs['class'] = "form-control input-sm"
AuthenticationForm.base_fields['password'].widget.attrs['placeholder'] = 'Password'


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^howto/(?P<name>.*)/$', 'main.views.howto', name='howto'),
    url(r'^orders/', include('orders.urls')),
    url(r'^committee/$', 'main.views.committee', name='committee'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/signup/', 'django.views.defaults.page_not_found'),
    url(r'^accounts/', include('allauth.urls')),
)
