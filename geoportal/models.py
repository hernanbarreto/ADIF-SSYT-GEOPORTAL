#from django.db import models
from django.contrib.gis.db import models

# Creates polygon layer in database
class Shapefile(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=25)
  geom = models.MultiPolygonField()
  objects = models.GeoManager()

  def __str__(self):
    return 'Name: %s' % self.name

# Creates line layer in database
class ShapefileLine(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=25)
  geom = models.MultiLineStringField()
  objects = models.GeoManager()

  def __str__(self):
    return 'Name: %s' % self.name

# Creates point layer in database
class ShapefilePoint(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=25)
  geom = models.PointField()
  objects = models.GeoManager()

  def __str__(self):
    return 'Name: %s' % self.name

# create new layers here, class should contain all atributes and geometry from shapefile
