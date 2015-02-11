from django.shortcuts import render_to_response
from django.contrib.gis.shortcuts import render_to_kml
from geoportal.models import *

# create kml files from shapefiles in db
def shpPoly(request):
  polygons = Shapefile.objects.kml()
  return render_to_kml("placemarks.kml", {'places': polygons})

def shpLine(request):
  lines = ShapefileLine.objects.kml()
  return render_to_kml("placemarks.kml", {'places': lines})

def shpPoint(request):
  points = ShapefilePoint.objects.kml()
  return render_to_kml("placemarks.kml", {'places': points})

# renders map template
def index(request):
  return render_to_response("map.html")
