#from django.db import models
from django.contrib.gis.db import models
from colorfield.fields import ColorField

# crea Poligonos
class Shapefile(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length = 50)
  color = ColorField()
  geom = models.MultiPolygonField()
  objects = models.GeoManager()

  def __unicode__(self):
    return 'Name: %s Id: %s' % (self.name, self.id) 

# crea Lineas
class ShapefileLine(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length = 50)
  color = ColorField()
  geom = models.MultiLineStringField()
  objects = models.GeoManager()

  def __unicode__(self):
    return 'Name: %s Id: %s' % (self.name, self.id) 

# crea Puntos
class ShapefilePoint(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length = 50)
  color = ColorField()
  geom = models.PointField()
  objects = models.GeoManager()

  def __unicode__(self):
    return 'Name: %s Id: %s' % (self.name, self.id)

#Posicion de los Andenes
class PosicionAnden (models.Model):
  posicion = models.CharField(max_length = 50)
  #posiciones: descendente, ascemdemte, central

  def __unicode__(self):
    return 'Posicion: %s' % (self.posicion)

# crea Tipo de estaciones
class TipoEstaciones (models.Model):
  tipo = models.CharField(max_length = 50)
  #Tipos: Intermedia, Trasbordo, terminal

  def __unicode__(self):
    return 'Name: %s' % (self.tipo)

# crea Estaciones
class Estaciones (models.Model):
  name = models.CharField(max_length = 50)
  anden = models.OneToOneField(Shapefile)
  posicion = models.OneToOneField(PosicionAnden)

  def __unicode__(self):
    return 'Name: %s' % (self.name)

