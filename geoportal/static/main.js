var map;


function init(){
	map = new ol.Map({
		target:'map',
		renderer:'canvas',
		view: new ol.View({
			projection: 'EPSG:3857',
			center: ol.proj.transform([19, 52], 'EPSG:4326', 'EPSG:3857'),
			zoom:6,
		})
	});
	var osm = new ol.layer.Tile({
	    source: new ol.source.OSM()
	});

	//map.addLayer(osm);

  // Polygon Layer
var PolygonLayer = new ol.layer.Vector({
  title: 'Poygon',
	source: new ol.source.KML({
		projection:new ol.proj.get("EPSG:3857"),
    url:'http://localhost:8000/poly/',
    extractStyles: false
	}),

  style: new ol.style.Style({
    fill: new ol.style.Fill({color: 'green'}),
    stroke: new ol.style.Stroke({color: 'red', width: 2})
  }),
});
map.addLayer(PolygonLayer);

  // Point Layer
var LineLayer = new ol.layer.Vector({
  title: 'Line',
	source: new ol.source.KML({
		projection:new ol.proj.get("EPSG:3857"),
    url:'http://localhost:8000/line/',
    extractStyles: false
	}),

  style: new ol.style.Style({
    stroke: new ol.style.Stroke({color: 'blue', width: 6})
  }),
});
map.addLayer(LineLayer);

  // Line Layer
var PointLayer = new ol.layer.Vector({
  title: 'Point',
	source: new ol.source.KML({
		projection:new ol.proj.get("EPSG:3857"),
    url:'http://localhost:8000/point/',
    extractStyles: false
	}),
  style: (function() {
  var textStroke = new ol.style.Stroke({
    color: 'yellow',
    width: 3
  });
  var textFill = new ol.style.Fill({
    color: 'black'
  });
  return function(feature, resolution) {
    return [new ol.style.Style({
      image: new ol.style.Circle({
      radius: 7,
      fill: new ol.style.Fill({color: 'yellow'}),
      stroke: new ol.style.Stroke({color: 'red'})
    }),
      text: new ol.style.Text({
        font: '11px arial,sans-serif',
        text: feature.get('name'),
        fill: textFill,
        stroke: textStroke,
        offsetX: 25,
        offsetY: -10
      })
    })];
  };
})()

});
map.addLayer(PointLayer);

// layer switcher
var switcher = new ol.control.LayerSwitcher({tipLabel: 'Legend'});
map.addControl(switcher);
}

