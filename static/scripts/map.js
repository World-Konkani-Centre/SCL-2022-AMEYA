let curLatLang = [12.985409023466968, 77.58148936513626];
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

map.panTo(new L.LatLng(12.947962836536151, 77.57231830099437));
var marker = L.marker([12.947962836536151, 77.57231830099437], {
  icon: new LeafIcon({
    iconUrl: `${window.location.origin}/static/icons/my-location.png`,
  }),
}).addTo(map);
marker.bindPopup("<b>Hello world!</b><br>I am a popup.");
L.circle([12.947962836536151, 77.57231830099437], { radius: 100 }).addTo(map);

// Create markers:
food.forEach((e) => {
  L.marker(e, {
    icon: new LeafIcon({
      iconUrl: `${window.location.origin}/static/icons/restaurant.png`,
    }),
  }).addTo(map);
});

shops.forEach((e) => {
  L.marker(e, {
    icon: new LeafIcon({
      iconUrl: `${window.location.origin}/static/icons/shop.png`,
    }),
  }).addTo(map);
});

bus.forEach((e) => {
  L.marker(e, {
    icon: new LeafIcon({
      iconUrl: `${window.location.origin}/static/icons/bus.png`,
    }),
  }).addTo(map);
});

L.Routing.control({
  waypoints: [
    L.latLng(...curLatLang),
    L.latLng(15.823532842591865, 74.5033861005741),
    L.latLng(15.819472137774307, 74.50183027558413),
    L.latLng(15.818778585138219, 74.50519060954872),
  ],
}).addTo(map);

// Get user geolocation:
// if ("geolocation" in navigator) {
//   navigator.geolocation.getCurrentPosition(function (pos) {
//     console.log(pos.coords.latitude, pos.coords.longitude);
//     curLatLang = [pos.coords.latitude, pos.coords.longitude];
//     loadMap(curLatLang);
//   });
// } else {
//   alert("Browser doesnot support geolocation");
// }

// Load User Location:
// function loadMap() {
//   map.panTo(new L.LatLng(...curLatLang));
//   var marker = L.marker(curLatLang, {
//     icon: new LeafIcon({
//       iconUrl: `${window.location.origin}/static/icons/my-location.png`,
//     }),
//   }).addTo(map);
//   marker.bindPopup("<b>Hello world!</b><br>I am a popup.");
//   L.circle(curLatLang, { radius: 200 }).addTo(map);

//   L.Routing.control({
//     waypoints: [
//       L.latLng(pos.coords.latitude, pos.coords.longitude),
//       L.latLng(15.823532842591865, 74.5033861005741),
//       L.latLng(15.819472137774307, 74.50183027558413),
//       L.latLng(15.818778585138219, 74.50519060954872),
//     ],
//   }).addTo(map);
// }
