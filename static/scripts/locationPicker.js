let curLatLng = [12.98524495891317, 77.58443296741585];
let latlng;
let m = undefined;
let lat = document.getElementById("latitude").value;
let lng = document.getElementById("longitude").value;
var map = L.map("map").setView(curLatLng, 15);
L.tileLayer("https://tile.osm.ch/switzerland/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);
L.Control.geocoder().addTo(map);

// Map click event listener:
map.on("click", function (e) {
  latlng = e.latlng;
  if (m) {
    map.removeLayer(m);
  }
  m = L.marker(latlng).addTo(map);

  map.setView(latlng);
});

// To set the map when container size changes
document
  .querySelector(".btn-picklocation")
  .addEventListener("click", function () {
    setTimeout(function () {
      if (m) map.removeLayer(m);
      if (lat && lng) {
        curLatLng = [lat, lng];
        m = L.marker(curLatLng).addTo(map);
      }
      map.setView(curLatLng, 15);
      map.invalidateSize();
    }, 1000);
  });

document.querySelector(".btn-picksave").addEventListener("click", function () {
  document.getElementById("latitude").value = latlng.lat;
  document.getElementById("longitude").value = latlng.lng;
});

document.querySelector(".btn-pickclear").addEventListener("click", function () {
  map.removeLayer(m);
});
