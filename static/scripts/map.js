let curLatLang = [12.933969688632496, 77.61193685079267];
let routeCoordinates = [];

var map = L.map("map").setView(curLatLang, 13);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "© OpenStreetMap",
}).addTo(map);

// Icon Class:
var LeafIcon = L.Icon.extend({
  options: {
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
  },
});

// Get user geolocation:
function getCurrLoc() {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (pos) {
      console.log(pos.coords.latitude, pos.coords.longitude);
      curLatLang = [pos.coords.latitude, pos.coords.longitude];
      // loadMap(curLatLang);
    });
  } else {
    alert("Browser doesnot support geolocation");
  }
}
function currentLocMarker(curLoc) {
  // var marker = L.marker(curLoc, {
  //   icon: new LeafIcon({
  //     iconUrl: `${window.location.origin}/static/icons/map/my-location.png`,
  //   }),
  // }).addTo(map);
  // marker.bindPopup("I am here");
  L.circle(curLoc, { radius: 100 }).addTo(map);
  map.panTo(new L.LatLng(...curLoc));
}

function fitMarkers(markers) {
  var group = new L.featureGroup(markers);
  map.fitBounds(group.getBounds());
}

function addMarker(latLng, icon) {
  var marker = L.marker(latLng, {
    icon: new LeafIcon({
      iconUrl: `${window.location.origin}/static/icons/map/${icon}.png`,
    }),
  }).addTo(map);
}

function addMarkers(data, icon) {
  markers = [];
  data.forEach((e) => {
    m = L.marker(e, {
      icon: new LeafIcon({
        iconUrl: `${window.location.origin}/static/icons/map/${icon}.png`,
      }),
    }).addTo(map);
    markers.push(m);
  });
  fitMarkers(markers);
}

// Data:
const food = [
  [12.947445452987786, 77.57142971731719],
  [12.947167112379699, 77.57143991737327],
  [12.947431221203333, 77.5739073344411],
  [12.948810777194627, 77.57431052476369],
  [12.947473932044836, 77.5743937923248],
  [12.946132904449533, 77.5706748048954],
];
const shops = [
  [12.948036643108097, 77.56988873020589],
  [12.94802260364985, 77.5698429218563],
  [12.948070892220445, 77.57017118002487],
  [12.947825827627968, 77.57053288336533],
  [12.94768779637963, 77.57018876744034],
];
const bus = [
  [12.948148105785773, 77.5705801862596],
  [12.94832204950334, 77.57066942725174],
  [12.948424369280499, 77.57357238423153],
  [12.948250425634344, 77.57367212416393],
  [12.949191766273346, 77.57360388117644],
  [12.949324781511196, 77.57379811157111],
];
addMarkers(food, "restaurant");
addMarkers(bus, "bus");
addMarkers(shops, "shop");

// map.panTo(new L.LatLng(12.947962836536151, 77.57231830099437));
// var marker = L.marker([12.947962836536151, 77.57231830099437], {
//   icon: new LeafIcon({
//     iconUrl: `${window.location.origin}/static/icons/map/my-location.png`,
//   }),
// }).addTo(map);
// marker.bindPopup("<b>Hello world!</b><br>I am a popup.");
// L.circle([12.947962836536151, 77.57231830099437], { radius: 100 }).addTo(map);

// const routing = L.Routing.control({
//   waypoints: [
//     L.latLng(15.823532842591865, 74.5033861005741),
//     L.latLng(15.819472137774307, 74.50183027558413),
//     L.latLng(15.818778585138219, 74.50519060954872),
//   ],
//   // ,show:false
// })
//   .on("routesfound", function (e) {
//     // showDirections(e);
//   })
//   .addTo(map);

// const mapDir = document.getElementById("pills-directions");
// var routingControlContainer = routing.getContainer();
// var controlContainerParent = routingControlContainer.parentNode;
// controlContainerParent.removeChild(routingControlContainer);
// mapDir.appendChild(routingControlContainer.childNodes[0]);

// Functions:
// function showDirections(e) {
//   const inst = e.routes[0].instructions;
//   console.log(e);
//   inst.forEach((i) => {
//     mapDir.insertAdjacentHTML("beforeend", `<div><p>${i.text}</p></div>`);
//   });
// }

function createWaypoints(latLngArr) {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (pos) {
      curLatLang = [pos.coords.latitude, pos.coords.longitude];
      latLngArr = [curLatLang, ...latLngArr];
      addMarkers(latLngArr, "marker");
      latLngArr = latLngArr.map((l) => L.latLng(...l));
      const routing = L.Routing.control({
        waypoints: latLngArr,
        createMarker: function () {
          return null;
        },
      })
        .on("routesfound", (e) => {
          routeCoordinates = e.routes[0].coordinates;
          getNearByRestaurants(routeCoordinates);
        })
        .addTo(map);
      currentLocMarker(curLatLang);
      const mapDir = document.getElementById("pills-directions");
      var routingControlContainer = routing.getContainer();
      var controlContainerParent = routingControlContainer.parentNode;
      controlContainerParent.removeChild(routingControlContainer);
      mapDir.appendChild(routingControlContainer.childNodes[0]);
    });
  } else {
    alert("Browser doesnot support geolocation");
  }
}

// MAP API:
function getTour(id) {
  const url = `${window.location.origin}/api/v1/tour/${+id}`;
  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      data = JSON.parse(data);
      return data;
    })
    .catch((err) => console.log(err));
}

function getDummyLatLng() {
  const url = `${window.location.origin}/api/v1/restaurants/dummy`;
  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      data = JSON.parse(data);
      data = data.map((e) => e.fields.latLng.split(","));
      addMarkers(data, "restaurant");
      console.log(data);
      return data;
    })
    .catch((err) => console.log(err));
}
getDummyLatLng();

function getNearByRestaurants(data) {
  const url = `${window.location.origin}/api/v1/restaurants/nearby`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => {
      data = JSON.parse(data);
      console.log(data);
      return data;
    })
    .catch((err) => console.log(err));
}
