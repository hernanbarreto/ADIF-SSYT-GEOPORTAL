from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from geoportal.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geodjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # kml files are now available:
    url(r'^poly/$', shpPoly),
    url(r'^line/$', shpLine),
    url(r'^point/$', shpPoint),
    url(r'^upload/$', upload, name="upload-kml"),                           
    url(r'^$', index, name = "index"),
    url(r'^admin/', include(admin.site.urls)),                       
)
