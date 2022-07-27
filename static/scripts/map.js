// Global Variables:
let tourId;
let recMarker = null;
let recRouting = null;
let curLatLang = [12.933969688632496, 77.61193685079267];
let routeCoordinates = [];
let tourCoordinates = [];
let nearby = [];
let recommendations = {};
const baseURL = `${window.location.origin}/api/v1`;
starIcon = `${window.location.origin}/static/icons/map/star.png`;

// Map Initialization:
var map = L.map("map").setView(curLatLang, 13);
L.tileLayer("https://tile.osm.ch/sswitzerland/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
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
        `<div class="map-popup nearby-popup"><div class="map-popup-header"><h3>${e.name}</h3><p>Rating: ${e.rating} <img width="15px" src=${starIcon} alt="stars"/></p></div> <img class="map-popup-image" src="/media/${e.image}"/><p>${e.description}</p></div>`
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
          `<div class="map-popup dest-popup"><div class="map-popup-header"><h3>${data.name}</h3><p>Rating: ${data.rating} <img width="18px" src=${starIcon} alt="stars"/></p></div><img class="map-popup-image" src="/media/${data.image}"/><p>${data.description}</p></div>`
        )
        .addTo(map);
    })
    .catch((err) => console.log(err));
}

// Add Recommendations marker to map:
function addRecommendationMarker(cat, id) {
  data = recommendations[cat][id];
  let latLng = [data.lat, data.lng];
  if (recMarker) map.removeLayer(recMarker);
  recMarker = new L.marker(latLng, {
    icon: new LeafIcon({
      iconUrl: `${window.location.origin}/static/icons/map/marker.png`,
    }),
  })
    .bindPopup(
      `<div class="map-popup rec-popup"><div class="map-popup-header"><h3>${data.name}</h3><p>Rating: ${data.rating} <img width="15px" src=${starIcon} alt="stars"/></p></div><img class="map-popup-image" src="/media/${data.image}"/><p>${data.description}</p></div>`
    )
    .addTo(map);
  recMarker.openPopup();
  map.panTo(latLng);
}

// Remove multiple markers from map:
function removeMarkers(data) {
  data.forEach((e) => {
    map.removeLayer(e);
  });
}

// Create Waypoints route:
function createWaypoints(latLngArr, id) {
  tourId = id;
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

// Create a waypoint route for recommendation
function createRecWaypoints(cat, id) {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (pos) {
      // Create an array of start and end points:
      rec = recommendations[cat][id];
      addRecommendationMarker(cat, id);
      recMarker.closePopup();
      curLatLang = [pos.coords.latitude, pos.coords.longitude];
      let latLngArr = [curLatLang, [rec.lat, rec.lng]];
      recCoordinates = latLngArr;
      latLngArr = latLngArr.map((l) => L.latLng(...l));
      // Create a route:
      if (recRouting) map.removeControl(recRouting);
      recRouting = L.Routing.control({
        waypoints: latLngArr,
        lineOptions: {
          styles: [{ color: "#58D68D", opacity: 1, weight: 5 }],
        },
        createMarker: function () {
          return null;
        },
      })
        .on("routesfound", (e) => {
          recRouteCoordinates = e.routes[0].coordinates;
        })
        .addTo(map);
      // Add directions to side panel:
      if (screen.width > 768) {
        let mapDir = document.getElementById("pills-directions");
        var routingControlContainer = recRouting.getContainer();
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

const addToWishlistBtn = document
  .querySelector(".btn-wishlist")
  .addEventListener("click", (e) => {
    option=e.target.getAttribute("data-wishlist");
    addToWishlist(option);
  });
// Recommendation Btn handler:
document.querySelectorAll("#pills-reco .nav-link").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    let cat;
    if (e.target.tagName === "IMG") {
      cat = e.target.parentElement.getAttribute("data-category");
    } else {
      cat = e.target.getAttribute("data-category");
    }
    getRecommendations(cat);
  });
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
      if (data.length === 0) return;
      nearby = addMarkersWithPopup(data, icon);
    })
    .catch((err) => console.log(err));
}

// POST request to get nearby recommendations:
function getRecommendations(cat) {
  tab = document.querySelector(`#pills-${cat}`);
  if (recommendations[cat]) return;
  tab.innerHTML = `<div class="card">
  <div class="header">
    <div class="details">
      <span class="name"></span>
    </div>
  </div>
  <div class="card-body">
    <div class="img"></div>
    <div class="description">
      <div class="line line-1"></div>
      <div class="line line-2"></div>
      <div class="line line-3"></div>
      <div class="line line-4"></div>
      <div class="line line-5"></div>
    </div>
  </div>
</div>
<div class="card">
  <div class="header">
    <div class="details">
      <span class="name"></span>
    </div>
  </div>
  <div class="card-body">
    <div class="img"></div>
    <div class="description">
      <div class="line line-1"></div>
      <div class="line line-2"></div>
      <div class="line line-3"></div>
      <div class="line line-4"></div>
      <div class="line line-5"></div>
    </div>
  </div>
</div>
<div class="card">
  <div class="header">
    <div class="details">
      <span class="name"></span>
    </div>
  </div>
  <div class="card-body">
    <div class="img"></div>
    <div class="description">
      <div class="line line-1"></div>
      <div class="line line-2"></div>
      <div class="line line-3"></div>
      <div class="line line-4"></div>
      <div class="line line-5"></div>
    </div>
  </div>
</div>
`;
  let data = {
    tourCoordinates,
    center: getCenter(tourCoordinates),
  };
  const url = `${baseURL}/recommendations/${cat}/`;
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
      recommendations[cat] = data;
      tab.innerHTML = "";
      if (data.length === 0) {
        tab.innerHTML = `<div class="rec-not-found">
        <img src="/static/icons/map/${cat}_rec.png" alt="Image-${cat}" />
        <h5>No Recommendations</h5>
      </div>`;
      }
      data.forEach((d, key) => {
        tab.insertAdjacentHTML(
          "beforeend",
          `<div class="rec-card">
        <div class="rec-header">
          <h4>${d.name}</h4>
        </div>
        <div class="rec-card-body">
          <img src="/media/${d.image}" alt="Image-${d.name}" class="rec-img">
          <div class="rec-description">
            <p>${d.description}</p>
          </div>
          <div class="rec-btns">
            <button class="rec-btn" onClick="createRecWaypoints('${cat}','${key}');">Directions</button>
            <button class="rec-btn" onClick="addRecommendationMarker('${cat}','${key}');">View</button>
          </div>
        </div>
        </div>`
        );
      });
    })
    .catch((err) => console.log(err));
}

// POST request to add tour to wishlist:
function addToWishlist(option) {
  const url = `${baseURL}/tour/addToWishlist/`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tourId,option }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        document.querySelector(".btn-wishlist").setAttribute("data-wishlist", "remove");
        document.querySelector(".btn-wishlist").innerHTML = `<img src="/static/icons/map/wishlist_added.png" alt="wishlist" class="btn-wishlist" data-wishlist="remove"/>`;
      } else {
        document.querySelector(".btn-wishlist").setAttribute("data-wishlist", "add");
        document.querySelector(".btn-wishlist").innerHTML = `<img src="/static/icons/map/wishlist_add.png" alt="wishlist" class="btn-wishlist" data-wishlist="add"/>`;
      }
    })
    .catch((err) => console.log(err));
}
