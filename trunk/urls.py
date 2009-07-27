from django.conf.urls.defaults import *
from frontend import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)
