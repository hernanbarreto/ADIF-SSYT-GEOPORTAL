Simple Geoportal
=============
Simple Geodjango application to display spatial data with Openlayers. Layers are stored in spatial database (postgis) and rendered to kml files with django. Kml files are displayed on the map with js openlayers.

Related links: [Geodjango](https://docs.djangoproject.com/en/1.7/ref/contrib/gis/), [Openlayers 3](http://openlayers.org), [Openlayers layer switcher](https://github.com/walkermatt/ol3-layerswitcher), [Postgis](https://github.com/walkermatt/ol3-layerswitcher).

#### Installation:
In *settings.py* setup your postgres database and run:

`python manage.py syncdb`

Create tables with spatial data in database:

`python manage.py makemigrations geoportal   `

`python manage.py sqlmigrate geoportal 0001   `

`python manage.py migrate   `

Add shapefiles to database.

To use different shapefiles, modify *models.py* first. To change layers styles and add controls, edit */static/main.js*.

To run application type:
`python manage.py runserver`

####Default view:

![img](http://i.imgur.com/MU2HOe6.png)