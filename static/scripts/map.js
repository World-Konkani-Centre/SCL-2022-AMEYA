// Global Variables:
let tourId;
let tourData;
let routing = null;
let recMarker = null;
let recRouting = null;
let curLatLang = [12.933969688632496, 77.61193685079267];
let routeCoordinates = [];
let tourRouteData = [];
let routeMarkers = [];
let tourCoordinates = [];
let nearby = [];
let recommendations = {};
const baseURL = `${window.location.origin}/api/v1`;
starIcon = `${window.location.origin}/static/icons/map/star.png`;
// Selectors:
const recPanel = document.getElementById("recommendation-panel");
const editPanel = document.querySelector(".edit-tour-panel");

// Map Initialization:
var map = L.map("map").setView(curLatLang, 13);
L.tileLayer("https://tile.osm.ch/switzerland/{z}/{x}/{y}.png", {
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
    mapAlert("Geolocation is not supported by this browser.", "danger");
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
  if (data.length === 0) {
    return [parseFloat(tourData.lat), parseFloat(tourData.lng)];
  }
  lat = (parseFloat(data[0][0]) + parseFloat(data[1][0])) / 2;
  lng = (parseFloat(data[0][1]) + parseFloat(data[1][1])) / 2;
  return [lat, lng];
}

// Add a single marker to map:
function addMarkerWithPopup(data) {
  hideRecPanel();
  m = L.marker([data.lat, data.lng], {
    icon: new LeafIcon({
      iconUrl: `${window.location.origin}/static/icons/map/marker.png`,
    }),
  })
    .bindPopup(
      `<div class="map-popup nearby-popup"><div class="map-popup-header"><h3>${
        data.name
      }
    ${
      data.type
        ? '<p class="verified-biz"><img src="/static/icons/map/verified.png" alt="Verified" />verified</p>'
        : ""
    }</h3>
    <p class="map-popup-rating">Rating: ${
      data.rating
    } <img width="15px" src=${starIcon} alt="stars"/></p></div> <img class="map-popup-image" src="${
        data.type ? data.banner : data.image
      }"/><p>${data.description}</p></div>`
    )
    .addTo(map);
  return m;
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
        `<div class="map-popup nearby-popup"><div class="map-popup-header"><h3>${
          e.name
        }
        ${
          e.type
            ? '<p class="verified-biz"><img src="/static/icons/map/verified.png" alt="Verified" />verified</p>'
            : ""
        }</h3>
        <p class="map-popup-rating">Rating: ${
          e.rating
        } <img width="15px" src=${starIcon} alt="stars"/></p></div> <img class="map-popup-image" src="${
          e.type ? e.banner : e.image
        }"/><p>${e.description}</p></div>`
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
      data.id = id;
      data.category = "destination";
      data.image = "/media/" + data.image;
      tourData = data;
      recommendations["destination"] = [tourData];
      tourRouteData.push({ cat: "destination", id: id });
      m = new L.marker(latlng, {
        icon: new LeafIcon({
          iconUrl: `${window.location.origin}/static/icons/map/marker.png`,
        }),
      })
        .bindPopup(
          `<div class="map-popup dest-popup"><div class="map-popup-header"><h3>${data.name}</h3><p class="map-popup-rating">Rating: ${data.rating} <img width="18px" src=${starIcon} alt="stars"/></p></div><img class="map-popup-image" src="${data.image}"/><p>${data.description}</p></div>`
        )
        .addTo(map);
      navigator.permissions &&
        navigator.permissions
          .query({ name: "geolocation" })
          .then(function (PermissionStatus) {
            if (PermissionStatus.state !== "granted") {
              m.openPopup();
              map.panTo(latlng);
            }
          });
    })
    .catch((err) => mapAlert("Failed to load tour details", "danger"));
}

// Add Recommendations marker to map:
function addRecommendationMarker(cat, id) {
  data = recommendations[cat][id];
  let latLng = [data.lat, data.lng];
  if (recMarker) map.removeLayer(recMarker);
  hideRecPanel();
  recMarker = new L.marker(latLng, {
    icon: new LeafIcon({
      iconUrl: `${window.location.origin}/static/icons/map/marker.png`,
    }),
  })
    .bindPopup(
      `<div class="map-popup rec-popup"><div class="map-popup-header"><h3>${
        data.name
      }
      ${
        data.type
          ? '<p class="verified-biz"><img src="/static/icons/map/verified.png" alt="Verified" />verified</p>'
          : ""
      }</h3>
      <p class="map-popup-rating">Rating: ${
        data.rating
      } <img width="15px" src=${starIcon} alt="stars"/></p></div> <img class="map-popup-image" src="${
        data.type ? data.banner : data.image
      }"/><p>${data.description}</p></div>`
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

// Add a multiple route markers to map:
function addRouteMarkers() {
  let m;
  removeMarkers(routeMarkers);
  tourRouteData.forEach((e) => {
    if (e.cat === "destination") return;
    let item = recommendations[e.cat].find((i) => i.id == e.id);
    if (item) {
      m = addMarkerWithPopup(item);
    }
    routeMarkers.push(m);
  });
  // fitMarkers(routeMarkers);
}

// Create Waypoints route:
function createWaypoints(latLngArr, destCoords, id) {
  tourId = id;
  m = addDestinationMarker(destCoords, tourId);
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (pos) {
      // Create an array of start and end points:
      curLatLang = [pos.coords.latitude, pos.coords.longitude];
      // convert array stored as string to array:
      if (typeof latLngArr === "string") {
        latLngArr = latLngArr.replace(/&#x27;/g, "'");
        latLngArr = latLngArr.replace(/^"|"$/g, "");
        latLngArr = latLngArr.replace(/'/g, '"');
        latLngArr = JSON.parse(latLngArr);
        latLngArr = [curLatLang, ...latLngArr];
      } else {
        latLngArr = [curLatLang, [...latLngArr]];
      }
      tourCoordinates = latLngArr;
      latLngArr = latLngArr.map((l) => L.latLng(...l));
      // Create a route:
      mapAlert("Finding best route...", "info");
      routing = L.Routing.control({
        waypoints: latLngArr,
        lineOptions: {
          styles: [{ color: "#3498DB", opacity: 1, weight: 7 }],
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
      let dirTab = routing.onAdd(map);
      document.getElementById("pills-directions").appendChild(dirTab);
    });
  } else {
    mapAlert("Geolocation is not supported by this browser.", "danger");
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
      mapAlert("Finding best route...", "info");
      recRouting = L.Routing.control({
        waypoints: latLngArr,
        lineOptions: {
          styles: [{ color: "#FF763A", opacity: 1, weight: 5 }],
          // styles: [{ color: "#58D68D", opacity: 1, weight: 5 }],
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
      let dirTab = recRouting.onAdd(map);
      document.getElementById("pills-directions").appendChild(dirTab);
    });
  } else {
    mapAlert("Geolocation is not supported by this browser.", "danger");
  }
}

// Create a new waypoint route for the add to tour button:
function createAddWaypoints(lat, lng, cat, id, verified) {
  // Check whether the cat and id exist in the in tourRouteData array:
  let exists = tourRouteData.find((e) => e.cat == cat && e.id == id);
  if (exists) {
    mapAlert("You have already added this to your tour.", "danger");
    return;
  }
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (pos) {
      curLatLang = [pos.coords.latitude, pos.coords.longitude];
      let latLng = [lat, lng];
      tourCoordinates = [curLatLang, latLng, ...tourCoordinates.slice(1)];
      tourRouteData.push({ cat: cat, id: id, verified });
      addRouteMarkers();
      let latLngArr = tourCoordinates;
      latLngArr = latLngArr.map((l) => L.latLng(...l));
      // Create a route:
      if (routing) map.removeControl(routing);
      if (recRouting) map.removeControl(recRouting);
      mapAlert("Finding best route...", "info");
      routing = L.Routing.control({
        waypoints: latLngArr,
        lineOptions: {
          styles: [{ color: "#3498DB", opacity: 1, weight: 7 }],
        },
        createMarker: function () {
          return null;
        },
      })
        .on("routesfound", (e) => {
          addRouteCoordinates = e.routes[0].coordinates;
        })
        .addTo(map);
      // Add directions to side panel:
      updateEditPanel(tourRouteData);
      let dirTab = routing.onAdd(map);
      document.getElementById("pills-directions").appendChild(dirTab);
    });
  } else {
    mapAlert("Geolocation is not supported by this browser.", "danger");
  }
}

// Recalculate route:
function recalculateRoute() {
  if (routing) map.removeControl(routing);
  if (recRouting) map.removeControl(recRouting);
  if (recMarker) map.removeLayer(recMarker);
  mapAlert("Finding best route...", "info");
  addRouteMarkers();
  let latLngArr = tourCoordinates;
  latLngArr = latLngArr.map((l) => L.latLng(...l));
  // Create a route:
  routing = L.Routing.control({
    waypoints: latLngArr,
    lineOptions: {
      styles: [{ color: "#3498DB", opacity: 1, weight: 7 }],
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
  let dirTab = routing.onAdd(map);
  document.getElementById("pills-directions").appendChild(dirTab);
}

// Update edit panel with current tour data:
function updateEditPanel(tourRouteData) {
  // Clear previous data:
  document.querySelector(".btn-edit-tour").style.display = "block";
  editPanel.innerHTML = "";
  tourRouteData.forEach((e) => {
    let item = recommendations[e.cat].find((i) => i.id == e.id);
    if (item) {
      editPanel.insertAdjacentHTML(
        "afterbegin",
        `<div class="drop_card"  data-cat="${item.category}" data-id="${
          item.id
        }" data-verified="${e.verified}">
        <div class="drop_data">
            <img src="${item.type ? item.banner : item.image}" alt="${
          item.name
        }" class="drop_img">

            <div>
                <h1 class="drop_name">${item.name}</h1>
                <span class="drop_profession">${
                  item.category.charAt(0).toUpperCase() + item.category.slice(1)
                }</span>
            </div>
        </div>
            ${
              item.category !== "destination"
                ? `<div><img src="/static/icons/map/delete_btn.png" alt="delete" class="et-delete" onclick="removeTour('${item.category}','${item.id}');" /></div>`
                : ""
            }
    </div>`
      );
    }
  });
}

// Remove tour from side panel:
function removeTour(cat, id) {
  let index = tourRouteData.findIndex((e) => e.cat == cat && e.id == id);
  if (index > -1) {
    tourRouteData.splice(index, 1);
    updateEditPanel(tourRouteData);
  }
  // Delete coordinates from tourCoordinates array:
  let item = recommendations[cat].find((i) => i.id == id);
  let latLng = [item.lat, item.lng];
  let index2 = tourCoordinates.findIndex(
    (e) => e[0] == latLng[0] && e[1] == latLng[1]
  );
  if (index2 > -1) {
    tourCoordinates.splice(index2, 1);
  }
  recalculateRoute();
}

// Map Eventlisteners:

// Map alert handler:
function mapAlert(msg, type) {
  document
    .getElementById("map")
    .insertAdjacentHTML(
      "afterbegin",
      `<div class="alert alert-${type} map-alert alert-message" role="alert">${msg}</div>`
    );
}

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
    option = e.target.getAttribute("data-wishlist");
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
// Rec bar mobile handler:
document.querySelector(".rec-bar").addEventListener("click", (e) => {
  recPanel.classList.toggle("slide-rec-panel");
});
document.querySelectorAll("#pills-tour-reco .nav-link").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    showRecPanel();
  });
});

function hideRecPanel() {
  if (screen.width < 768) recPanel.classList.remove("slide-rec-panel");
}

function showRecPanel() {
  if (screen.width < 768) recPanel.classList.add("slide-rec-panel");
}

// Save Tour Btn handler:
document.querySelector(".et-save").addEventListener("click", (e) => {
  saveTour();
});

// MAP API:

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
      if (data.length === 0) throw new Error("No nearby locations found");
      nearby = addMarkersWithPopup(data, icon);
    })
    .catch((err) => mapAlert(err.message, "warning"));
}

// POST request to get nearby recommendations:
function getRecommendations(cat) {
  tab = document.querySelector(`#pills-${cat}`);
  tab.innerHTML = `<div class="card">
  <div class="header">
    <div class="details">
      <span class="name"></span>
      <span class="rating"></span>
    </div>
  </div>
  <div class="card-body">
    <div class="img"></div>
    <div class="description">
      <div class="line line-1"></div>
      <div class="line line-2"></div>
      <div class="line line-3"></div>
    </div>
    <div class="card-btns description">
    <div class="line line-4"></div>
    <div class="line line-5"></div>
    <div class="line line-6"></div>
    </div>
  </div>
</div>
`.repeat(3);
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
      console.log(data);
      if (recommendations[cat]) recommendations[cat].push(...data);
      else recommendations[cat] = data;
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
          ${
            d.type
              ? '<p class="verified-biz"><img src="/static/icons/map/verified.png" alt="Verified" />verified</p>'
              : ""
          }
          <p class="rec-card-rating">${
            d.rating
          } <img width="15px" src=${starIcon} alt="stars"/></p>
        </div>
        <div class="rec-card-body">
          <img src="${d.type ? d.banner : d.image}" alt="Image-${
            d.name
          }" class="rec-img">
          <div class="rec-description">
            <p>${d.description}</p>
          </div>
          <div class="rec-btns">
            <button class="rec-btn" onClick="createRecWaypoints('${cat}','${key}');">Directions</button>
            <button class="rec-btn" onClick="addRecommendationMarker('${cat}','${key}');">View</button>
            <button class="rec-btn" onClick="createAddWaypoints('${d.lat}','${
            d.lng
          }','${cat}','${d.id}',${d.type});">Add to tour</button>
          </div>
        </div>
        </div>`
        );
      });
    })
    .catch((err) => mapAlert(err.message, "danger"));
}

// POST request to add tour to wishlist:
function addToWishlist(option) {
  const url = `${baseURL}/tour/addToWishlist/`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tourId, option }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        document
          .querySelector(".btn-wishlist")
          .setAttribute("data-wishlist", "remove");
        document.querySelector(
          ".btn-wishlist"
        ).innerHTML = `<img src="/static/icons/map/wishlist_added.png" alt="wishlist" class="btn-wishlist" data-wishlist="remove"/>`;
        mapAlert("Tour added to wishlist", "success");
      } else {
        document
          .querySelector(".btn-wishlist")
          .setAttribute("data-wishlist", "add");
        document.querySelector(
          ".btn-wishlist"
        ).innerHTML = `<img src="/static/icons/map/wishlist_add.png" alt="wishlist" class="btn-wishlist" data-wishlist="add"/>`;
        mapAlert("Tour removed from wishlist", "success");
      }
    })
    .catch((err) => mapAlert(err.message, "danger"));
}

// POST request to save tour:
function saveTour() {
  const url = `${baseURL}/tour/save/`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      tourId,
      tourCoords: tourCoordinates.slice(1),
      tourRoute: tourRouteData,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        mapAlert("Tour saved", "success");
      } else {
        mapAlert("Something went wrong", "danger");
      }
    })
    .catch((err) => mapAlert(err.message, "danger"));
}

// Fetch Saved Tour data:
function getSavedTour(id) {
  const overlay = document.querySelector(".overlay");
  overlay.style.display = "flex";
  const url = `${baseURL}/tour/getSavedTour/`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        // Set a delay of 5secs to allow the map to load:
        recommendations = Object.assign(recommendations, data.rec);
        tourRouteData = data.route;
        setTimeout(() => {
          addRouteMarkers();
          updateEditPanel(tourRouteData);
          overlay.style.display = "none";
        }, 5000);
      } else {
        overlay.innerHTML = `<h3>Something Went Wrong!</h3>`;
      }
    })
    .catch((err) => (overlay.innerHTML = `<h3>Something Went Wrong!</h3>`));
}

// Edit Tour Panel sortable:
const dropItems = document.getElementById("drop-items");

new Sortable(dropItems, {
  animation: 300,
  chosenClass: "sortable-chosen",
  dragClass: "sortable-drag",
  // Update event:
  onUpdate: reArrangeRoute,
});

function reArrangeRoute() {
  let sortedRouteData = [];
  document.querySelectorAll(".drop_card").forEach((card) => {
    let item = {
      cat: card.getAttribute("data-cat"),
      id: card.getAttribute("data-id"),
      verified: card.getAttribute("data-verified") === "true" ? true : false,
    };
    sortedRouteData.push(item);
  });
  tourRouteData = sortedRouteData;
  reCreateTourCoordinates();
  recalculateRoute();
}

function reCreateTourCoordinates() {
  let newtourCoordinates = [];
  // get current location:
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      currLoc = [position.coords.latitude, position.coords.longitude];
      newtourCoordinates.push(currLoc);
      tourRouteData.forEach((item) => {
        let data = recommendations[item.cat].find((d) => d.id == item.id);
        newtourCoordinates.push([data.lat, data.lng]);
      });
      tourCoordinates = newtourCoordinates;
    });
  } else {
    mapAlert("Geolocation is not supported by this browser.", "danger");
  }
}
