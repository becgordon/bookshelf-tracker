'use strict';

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8, b
  });
}

window.initMap = initMap;

// { lat: 42.3265, lng: -122.8756 }