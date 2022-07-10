// Global Variables:
let curLatLang = [12.933969688632496, 77.61193685079267];
let routeCoordinates = [];
let tourCoordinates = [];
let nearby = [];
const baseURL = `${window.location.origin}/api/v1`;
starIcon = `${window.location.origin}/static/icons/map/star.png`;

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

var LeafIconLoc = L.Icon.extend({
  options: {
    iconSize: [16, 16],
    iconAnchor: [8, 8],
    popupAnchor: [0, -16],
  },
});

// Get user geolocation every second:
function getCurrLoc() {
  let loc = undefined;
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (pos) {
      curLatLang = [pos.coords.latitude, pos.coords.longitude];
      loc = currentLocMarker(curLatLang);
    });
    setInterval(() => {
      navigator.geolocation.getCurrentPosition(function (pos) {
        curLatLang = [pos.coords.latitude, pos.coords.longitude];
        if (loc) {
          map.removeLayer(loc.m);
          map.removeLayer(loc.c);
        }
        loc = currentLocMarker(curLatLang);
      });
    }, 5000);
  } else {
    alert("Browser doesnot support geolocation");
  }
}
// Add a marker to user location:
function currentLocMarker(curLoc) {
  m = L.marker(curLoc, {
    autoPan: false,
    icon: new LeafIconLoc({
      iconUrl: `${window.location.origin}/static/icons/map/loc.png`,
    }),
  })
    .bindPopup("<h6>You are here</h6>")
    .addTo(map);
  c = L.circle(curLoc, { radius: 100 }).addTo(map);
  return { m, c };
}
// Fit markers to screen:
function fitMarkers(markers) {
  var group = new L.featureGroup(markers);
  map.fitBounds(group.getBounds());
}
// Get center of start and end coordinates:
function getCenter(data) {
  lat = (parseFloat(data[0][0]) + parseFloat(data[1][0])) / 2;
  lng = (parseFloat(data[0][1]) + parseFloat(data[1][1])) / 2;
  return [lat, lng];
}

// Add a single marker to map:
function addMarker(latLng, icon) {
  var marker = L.marker(latLng, {
    icon: new LeafIcon({
      iconUrl: `${window.location.origin}/static/icons/map/${icon}.png`,
    }),
  }).addTo(map);
}

// Add multiple markers to map:
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
  return markers;
}

// Add multiple markers to map with popup details:
function addMarkersWithPopup(data, icon) {
  markers = [];
  data.forEach((e) => {
    m = L.marker([e.lat, e.lng], {
      title: e.name,
      icon: new LeafIcon({
        iconUrl: `${window.location.origin}/static/icons/map/${icon}.png`,
      }),
    })
      .bindPopup(
        `<h3>${e.name}</h3><p>Rating: ${e.rating} <img width="15px" src=${starIcon} alt="stars"/></p><p>${e.description}</p>`
      )
      .addTo(map);
    markers.push(m);
  });
  fitMarkers(markers);
  return markers;
}
// Add tour details popup marker to map:
function addDestinationMarker(latlng, id) {
  const url = `${baseURL}/tour/${+id}`;
  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      data = JSON.parse(data);
      data = data[0].fields;
      m = new L.marker(latlng, {
        icon: new LeafIcon({
          iconUrl: `${window.location.origin}/static/icons/map/marker.png`,
        }),
      })
        .bindPopup(
          `<h3>${data.name}</h3><p>Rating: ${data.rating} <img width="18px" src=${starIcon} alt="stars"/></p><img width="100%" height="auto" src="/media/${data.image}"/><p>${data.description}</p>`
        )
        .addTo(map);
    })
    .catch((err) => console.log(err));
}
// Remove multiple markers from map:
function removeMarkers(data) {
  data.forEach((e) => {
    map.removeLayer(e);
  });
}
// Dummy Data:
const food = [
  [12.947445452987786, 77.57142971731719],
  [12.947167112379699, 77.57143991737327],
  [12.947431221203333, 77.5739073344411],
  [12.948810777194627, 77.57431052476369],
  [12.947473932044836, 77.5743937923248],
  [12.946132904449533, 77.5706748048954],
];

// Create Waypoints route:
function createWaypoints(latLngArr, tourId) {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (pos) {
      // Create an array of start and end points:
      addDestinationMarker(latLngArr, tourId);
      curLatLang = [pos.coords.latitude, pos.coords.longitude];
      latLngArr = [curLatLang, [...latLngArr]];
      tourCoordinates = latLngArr;
      latLngArr = latLngArr.map((l) => L.latLng(...l));
      // Create a route:
      const routing = L.Routing.control({
        waypoints: latLngArr,
        lineOptions: {
          styles: [{ color: "#65b5ff", opacity: 1, weight: 5 }],
        },
        createMarker: function () {
          return null;
        },
      })
        .on("routesfound", (e) => {
          routeCoordinates = e.routes[0].coordinates;
        })
        .addTo(map);
      // Add directions to side panel:
      if (screen.width > 768) {
        let mapDir = document.getElementById("pills-directions");
        var routingControlContainer = routing.getContainer();
        var controlContainerParent = routingControlContainer.parentNode;
        controlContainerParent.removeChild(routingControlContainer);
        mapDir.appendChild(routingControlContainer.childNodes[0]);
      }
    });
  } else {
    alert("Browser doesnot support geolocation");
  }
}
// Map Eventlisteners:

// Nearby Btn toggler:
function nearbyHandler(e) {
  let cat;
  nearbyBtns.forEach((btn) => {
    btn.classList.remove("active-btn");
  });
  removeMarkers(nearby);
  if (e.target.tagName === "IMG") {
    cat = e.target.parentElement.getAttribute("data-a");
    e.target.parentNode.classList.add("active-btn");
  } else {
    cat = e.target.getAttribute("data-a");
    e.target.classList.add("active-btn");
  }
  getNearBy(cat);
}

const nearbyBtns = document.querySelectorAll(".nearby-btn");
nearbyBtns.forEach((btn) => {
  btn.addEventListener("click", nearbyHandler);
});

// MAP API:

// Get tour data by id:
function getTour(id) {
  const url = `${baseURL}/tour/${+id}`;
  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      data = JSON.parse(data);
      return data;
    })
    .catch((err) => console.log(err));
}

// function getDummyLatLng() {
//   const url = `${window.location.origin}/api/v1/restaurants/dummy`;
//   fetch(url)
//     .then((res) => res.json())
//     .then((data) => {
//       data = JSON.parse(data);
//       data = data.map((e) => [e.fields.lat, e.fields.lng]);
//       addMarkers(data, "restaurant");
//       return data;
//     })
//     .catch((err) => console.log(err));
// }

// POST request to get nearby locations:
function getNearBy(cat) {
  // Category selector:
  if (cat === "hotel") {
    route = "hotel";
    icon = "bed";
  } else if (cat === "repair") {
    route = "repair";
    icon = "spanner";
  } else {
    route = "restaurant";
    icon = "restaurant";
  }
  let data = {
    routeCoordinates,
    tourCoordinates,
    center: getCenter(tourCoordinates),
  };
  const url = `${baseURL}/nearby/${route}/`;
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
      data = data.map((d) => d.fields);
      console.log(data);
      nearby = addMarkersWithPopup(data, icon);
    })
    .catch((err) => console.log(err));
}
