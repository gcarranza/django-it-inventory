from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^capture_login/$', capture_login),
    (r'^/$', capture_login),
)
