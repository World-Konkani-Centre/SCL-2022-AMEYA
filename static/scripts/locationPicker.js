let curLatLng = [12.98524495891317, 77.58443296741585];
let latlng;
let m = undefined;
var map = L.map("map").setView(curLatLng, 15);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap",
}).addTo(map);
L.Control.geocoder().addTo(map);

// Map click event listener:
map.on("click", function (e) {
  latlng = e.latlng;
  if (m) {
    map.removeLayer(m);
  }
  m = L.marker(latlng).addTo(map);

<<<<<<< HEAD
  map.setView(latlng);
=======
  map.setView(latlng, 15);
>>>>>>> 435bd44723f39b4550e9798d399fcb234d2ea96a
});

// To set the map when container size changes
document
  .querySelector(".btn-picklocation")
  .addEventListener("click", function () {
    setTimeout(function () {
      map.setView(curLatLng, 15);
      map.invalidateSize();
    }, 1000);
  });

document.querySelector(".btn-picksave").addEventListener("click", function () {
  document.getElementById("latitude").value = latlng.lat;
  document.getElementById("longitude").value = latlng.lng;
});
