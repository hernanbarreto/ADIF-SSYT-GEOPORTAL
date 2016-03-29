from django.shortcuts import render_to_response
from django.contrib.gis.shortcuts import render_to_kml
from geoportal.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.contrib.gis.gdal import DataSource
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.gis.gdal import OGRGeometry
import json
import itertools
import tempfile
import os

from django.views.generic import TemplateView

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

def upload(request):
    if 'kml' in request.FILES:
        # Get
        try:
            kmlFile = request.FILES['kml']
        except IOError:
            print("kml")


        handle, targetPath = tempfile.mkstemp()
        destination = os.fdopen(handle, 'wb')
        for chunk in kmlFile.chunks():
            destination.write(chunk)
        destination.close()

        # Parse
        dataSource = DataSource(targetPath)

        layer = dataSource[0]
        try:
          Names = layer.get_fields('Name')
        except:
          Names = layer.get_fields('name')          
        Geometries = layer.get_geoms()

        # name change from Python 2 to 3
        try:
            zip_longest = itertools.zip_longest  # Python 3
        except AttributeError:
            zip_longest = itertools.izip_longest  # Python 2

        for Name, Geometry in zip_longest(Names, Geometries):
          if (str(layer.geom_type) == 'Point') or (str(layer.geom_type) == 'Point25D') or (str(layer.geom_type) == 'MultiPoint') or (str(layer.geom_type) == 'MultiPoint25D'):
            point = ShapefilePoint(id = ShapefilePoint.objects.count(), color = '#00ff00', name=Name, geom=Geometry.wkt)
            point.save()
          elif (str(layer.geom_type) == 'LineString') or (str(layer.geom_type) == 'LineString25D') or (str(layer.geom_type) == 'MultiLineString') or (str(layer.geom_type) == 'MultiLineString25D'):
            line = ShapefileLine(id = ShapefileLine.objects.count(), color = '#ff0000', name=Name, geom=Geometry.wkt)
            line.save()
          elif (str(layer.geom_type) == 'Polygon') or (str(layer.geom_type) == 'Polygon25D') or (str(layer.geom_type) == 'MultiPolygon') or (str(layer.geom_type) == 'MultiPolygon25D'):
            poly = Shapefile(id = Shapefile.objects.count(), color = '#0000ff', name=Name, geom=Geometry.wkt)
            poly.save()

        # Clean up: took out the os.remove(targetPath)


    return HttpResponseRedirect(reverse('index'))
  
# renders map template
#def index(request):
#  return render_to_response("map.html")
#def index(request):
#    waypoints = ShapefilePoint.objects.order_by('name')
#    template = loader.get_template('map.html')
#    context = RequestContext(request, {
#        'waypoints': waypoints, 'content': render_to_string('waypoints.html', {'waypoints': waypoints})
#    })
#    return HttpResponse(template.render(context))

def index(request):
  context = {}
  waypoints = ShapefilePoint.objects.order_by('name')
  lines = ShapefileLine.objects.order_by('name')
  polys = Shapefile.objects.order_by('name')    
  return render_to_response('map.html', {'waypoints': waypoints, 'lines': lines, 'polys': polys}, context_instance=RequestContext(request))
