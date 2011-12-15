from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'django_it_inventory.views.home', name='home'),
    # url(r'^django_it_inventory/', include('django_it_inventory.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^admin_export/', include("admin_export.urls")),
)

urlpatterns += patterns('', (r'^inventory/', include('django_it_inventory.it_inventory.urls')), )
