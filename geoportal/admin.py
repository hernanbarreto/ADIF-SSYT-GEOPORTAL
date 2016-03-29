#from django.contrib import admin
from django.contrib.gis import admin
from geoportal.models import *

# registered shapefiles are available in admin panel
admin.site.register(Shapefile, admin.OSMGeoAdmin)
admin.site.register(ShapefileLine, admin.OSMGeoAdmin)
admin.site.register(ShapefilePoint, admin.OSMGeoAdmin)

admin.site.register(TipoEstaciones)
admin.site.register(Estaciones)
admin.site.register(PosicionAnden)
