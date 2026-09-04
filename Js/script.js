import { locations, cities, details } from "./data.js";
import { createMap } from "./map.js";
import { addMarkers } from "./markers.js";

const map = createMap();

const cityMarkers = addMarkers(map, cities,"#37a746" );
const detailMarkers = addMarkers(map, details, "#8e99a5");
const locationMarkers = addMarkers(map, locations, "#37a746");

document.getElementById("close-map-details")?.addEventListener("click", () => {
  document.getElementById("map-details")?.classList.remove("is-visible");
});

cityMarkers.forEach(m => m.addTo(map));
detailMarkers.forEach(m => m.addTo(map));
locationMarkers.forEach(m => m.addTo(map));

cityMarkers.forEach((marker, i) => {

  marker.getElement().onclick = () => {
    const isMobile = window.matchMedia("(max-width: 600px)").matches;
    const mobileOffset = isMobile
      ? [0, -map.getContainer().clientHeight * 0.25]
      : [0, 0];

    map.flyTo({
      center: cities[i].coords,
      zoom: 12,
      offset: mobileOffset
    });
  };
});

