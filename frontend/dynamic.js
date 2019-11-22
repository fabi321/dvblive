var abschnitte = [];
async function getJsonAsync(name)
{
	let response = await fetch(`${name}`);
	let data = await response.json()
	return data;
}
getJsonAsync('abschnitte.json')
	.then(function(data) {
	for (i = 0; i < data.length; i++){
		var verbindung = data[i];
		var latlngs = [];
		for (latlon_count = 0; latlon_count < verbindung.polygon.length; latlon_count++){
		    latlngs.push([verbindung.polygon[latlon_count].latitude, verbindung.polygon[latlon_count].longitude])
		}
		var tooltip = "";
		for (tooltip_count = 0; tooltip_count < verbindung.linien.length; tooltip_count++){
			tooltip += "Linie " + verbindung.linien[tooltip_count] + "<br>";
		}
		var farbe = "green";
		if (verbindung.maxVerspaetung >= 60){
			farbe = "orange";
		}
		if (verbindung.maxVerspaetung >= 300){
			farbe = "red";
		}
		L.polyline(latlngs, {color: farbe}).addTo(mymap).bindTooltip(tooltip)
	}
}).then(getJsonAsync('haltestelle.json')
	.then(function(data) {
	for (i = 0; i < data.length; i++){
		var aktuelle_haltestelle = data[i]
        L.circle([aktuelle_haltestelle.latitude, aktuelle_haltestelle.longitude], {
           color: 'blue',
           fillColor: '#00c1ff',
           fillOpacity: 0.2,
           radius: 20
		}).addTo(mymap).bindTooltip(data[i].stopName);
	}
}));
