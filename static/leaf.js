var mymap = L.map('mapid').setView([51.512, -0.104], 12);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'ENTER YOUR ACCESS TOKEN HERE'
}).addTo(mymap);

var source = new EventSource('/topic/geodata4');
//var markers = L.layerGroup();
mapMarkers1 = [];
mapMarkers2 = [];

var greenIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

source.addEventListener('message', function(e){
  console.log('Message');
  obj = JSON.parse(e.data);
  console.log(obj)

  if (obj.busline == '00001') {
      for(var i = 0; i < mapMarkers1.length; i++){
        mymap.removeLayer(mapMarkers1[i]);
      }

      marker1 = L.marker([obj.latitude, obj.longitude],).addTo(mymap);
      mapMarkers1.push(marker1);
  }

  if (obj.busline == '00002') {
      for(var i = 0; i < mapMarkers2.length; i++){
        mymap.removeLayer(mapMarkers2[i]);
      }

      marker2 = L.marker([obj.latitude, obj.longitude],{icon: greenIcon}).addTo(mymap);
      mapMarkers2.push(marker2);
  }
}, false);
