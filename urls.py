from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^admin_export/', include("admin_export.urls")),
    (r'^inventory/', include('django-it-inventory.it_inventory.urls'))
)
