#from django.contrib import admin
from django.contrib.gis import admin
from geoportal.models import *

# registered shapefiles are available in admin panel
admin.site.register(Shapefile, admin.GeoModelAdmin)
admin.site.register(ShapefileLine, admin.GeoModelAdmin)
admin.site.register(ShapefilePoint, admin.GeoModelAdmin)
