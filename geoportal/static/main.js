var map;
var color;
var R, G, B;


function init(){
    var thunderforestAttributions = [
        new ol.Attribution({
            html: 'Tiles &copy; <a href="http://www.thunderforest.com/">Thunderforest</a>'
        }),
        ol.source.OSM.ATTRIBUTION
    ];

    map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Group({
                'title': 'Base maps',
                layers: [
                    new ol.layer.Tile({
                        title: 'Stamen - Water color',
                        type: 'base',
                        visible: false,
                        source: new ol.source.Stamen({
                            layer: 'watercolor'
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'Stamen - Toner',
                        type: 'base',
                        visible: false,
                        source: new ol.source.Stamen({
                            layer: 'toner'
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'MapQuest - OSM',
                        type: 'base',
                        visible: false,
                        source: new ol.source.MapQuest({
                            layer: 'osm'
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'MapQuest - Satellite',
                        type: 'base',
                        visible: false,
                        source: new ol.source.MapQuest({
                            layer: 'sat'
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'MapQuest - Hybrid',
                        type: 'base',
                        visible: false,
                        source: new ol.source.MapQuest({
                            layer: 'hyb'
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'Thunderforest - OpenCycleMap',
                        type: 'base',
                        visible: false,
                        source: new ol.source.OSM({
                            url: 'http://{a-c}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png',
                            attributions: thunderforestAttributions
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'Thunderforest - Outdoors',
                        type: 'base',
                        visible: false,
                        source: new ol.source.OSM({
                            url: 'http://{a-c}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png',
                            attributions: thunderforestAttributions
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'Thunderforest - Landscape',
                        type: 'base',
                        visible: false,
                        source: new ol.source.OSM({
                            url: 'http://{a-c}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',
                            attributions: thunderforestAttributions
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'Thunderforest - Transport',
                        type: 'base',
                        visible: false,
                        source: new ol.source.OSM({
                            url: 'http://{a-c}.tile.thunderforest.com/transport/{z}/{x}/{y}.png',
                            attributions: thunderforestAttributions
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'Thunderforest - Transport Dark',
                        type: 'base',
                        visible: false,
                        source: new ol.source.OSM({
                            url: 'http://{a-c}.tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png',
                            attributions: thunderforestAttributions
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'OSM',
                        type: 'base',
                        visible: true,
                        source: new ol.source.OSM()
                    })
                ]
            }),
            new ol.layer.Group({
                title: 'Overlays',
                layers: [
                    new ol.layer.Tile({
                        title: 'Countries',
                        source: new ol.source.TileWMS({
                            url: 'http://demo.opengeo.org/geoserver/wms',
                            params: {'LAYERS': 'ne:ne_10m_admin_1_states_provinces_lines_shp'},
                            serverType: 'geoserver'
                        })
                    })
                ]
            })
        ],
        view: new ol.View({
            center: ol.proj.transform([-59, -34.7], 'EPSG:4326', 'EPSG:3857'),
            zoom: 9
        })
	
    });

map.addControl(new ol.control.LayerSwitcher());
map.addControl(new ol.control.ScaleLine());

// Polygon Layer
for (i = 0; i <  parseInt(String(polyByID.length)); i++) {
//obtengo color y lo convierto a RGB

color = polyByID[i].color;
R = String(parseInt(color.substring(1, 3), 16));
G = String(parseInt(color.substring(3, 5), 16));
B = String(parseInt(color.substring(5, 7), 16));
color = "rgba(" + R + "," + G + "," + B + ", 0.3)"; 

//obtengo las coordenadas
polyByID[i].coord = polyByID[i].coord.split(",");
polyByID[i].coord.splice(polyByID[i].coord.length-1, 1);
for (j = 0; j< polyByID[i].coord.length; j++){
polyByID[i].coord[j] = polyByID[i].coord[j].replace("(", "");
polyByID[i].coord[j] = polyByID[i].coord[j].replace("(", "");
polyByID[i].coord[j] = polyByID[i].coord[j].replace("(", "");
polyByID[i].coord[j] = polyByID[i].coord[j].replace("(", "");
polyByID[i].coord[j] = polyByID[i].coord[j].replace(")", "");
polyByID[i].coord[j] = polyByID[i].coord[j].replace(")", "");
polyByID[i].coord[j] = polyByID[i].coord[j].replace(")", "");
polyByID[i].coord[j] = polyByID[i].coord[j].replace(")", "");
}
var pointList = [];
for (p = 0; p < parseInt((polyByID[i].coord.length)/2); p++){
 pointList.push(ol.proj.transform([parseFloat(polyByID[i].coord[2*p]),parseFloat(polyByID[i].coord[(2*p)+1])], 'EPSG:4326', 'EPSG:3857'));
}
var poligonsource = new ol.source.Vector({});
var PolygonLayer = new ol.layer.Vector({
  title: polyByID[i].name,
	source: poligonsource,

  style: new ol.style.Style({
    fill: new ol.style.Fill({color: color}),
    stroke: new ol.style.Stroke({color: color, width: 1})
  }),
});
var thing = new ol.geom.Polygon([pointList]);
var featurething = new ol.Feature({
    name: polyByID[i].name,
    geometry: thing
});
poligonsource.addFeature( featurething );
map.addLayer(PolygonLayer);
}

// Line Layer
for (i = 0; i <  parseInt(String(lineByID.length)); i++) {
//obtengo el color
color = lineByID[i].color;
R = String(parseInt(color.substring(1, 3), 16));
G = String(parseInt(color.substring(3, 5), 16));
B = String(parseInt(color.substring(5, 7), 16));
color = "rgba(" + R + "," + G + "," + B + ", 0.7)"; 

//obtengo las coordenadas
lineByID[i].coord = lineByID[i].coord.split(",");
lineByID[i].coord.splice(lineByID[i].coord.length-1, 1);
for (j = 0; j< lineByID[i].coord.length; j++){
lineByID[i].coord[j] = lineByID[i].coord[j].replace("(", "");
lineByID[i].coord[j] = lineByID[i].coord[j].replace("(", "");
lineByID[i].coord[j] = lineByID[i].coord[j].replace("(", "");
lineByID[i].coord[j] = lineByID[i].coord[j].replace(")", "");
lineByID[i].coord[j] = lineByID[i].coord[j].replace(")", "");
lineByID[i].coord[j] = lineByID[i].coord[j].replace(")", "");
}
var pointList = [];
for (p = 0; p < parseInt((lineByID[i].coord.length)/2); p++){
 pointList.push(ol.proj.transform([parseFloat(lineByID[i].coord[2*p]),parseFloat(lineByID[i].coord[(2*p)+1])], 'EPSG:4326', 'EPSG:3857'));
}

var linesource = new ol.source.Vector({});
var LineLayer = new ol.layer.Vector({
  title:lineByID[i].name,
	source: linesource,

  style: new ol.style.Style({
    stroke: new ol.style.Stroke({color: color, width: 2})
  }),
});
var thingline = new ol.geom.LineString(pointList);
var featurethingline = new ol.Feature({
    name: lineByID[i].name,
    geometry: thingline
});
linesource.addFeature( featurethingline );
map.addLayer(LineLayer);
}

// Capa de Puntos
for (i = 0; i <  parseInt(String(waypointByID.length)); i++) {
//obtengo el color
color = waypointByID[i].color;
R = String(parseInt(color.substring(1, 3), 16));
G = String(parseInt(color.substring(3, 5), 16));
B = String(parseInt(color.substring(5, 7), 16));
color = "rgba(" + R + "," + G + "," + B + ", 0.7)"; 

var pointsource = new ol.source.Vector({});
var PointLayer = new ol.layer.Vector({
  title: waypointByID[i].name,
  source: pointsource,
  style: new ol.style.Style({
	image: new ol.style.Circle({radius: 4, fill: new ol.style.Fill({color: color}), stroke: new ol.style.Stroke({color: color})}),
  text: new ol.style.Text({
        font: '11px arial,sans-serif',
        text: waypointByID[i].name,
        fill: new ol.style.Fill({color: 'black'}),
        stroke: new ol.style.Stroke({color: color, width: 1}),
        offsetX: 25,
        offsetY: -10
      })
  })
});
var thingPoint = new ol.geom.Point(ol.proj.transform(waypointByID[i].coord, 'EPSG:4326', 'EPSG:3857'));
var featurethingPoint = new ol.Feature({
    name: waypointByID[i].name,
    geometry: thingPoint
});
pointsource.addFeature( featurethingPoint );
map.addLayer(PointLayer);
}
}