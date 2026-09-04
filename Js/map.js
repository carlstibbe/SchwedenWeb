export function createMap() {

  const startCenter = [14.391464, 58.524548];
  const startZoom = 6.7;

  const map = new maplibregl.Map({
    container: 'map',
    style: {
        version: 8,
        sources: {
            esri: {
            type: "raster",
            tiles: [
                "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            ],
            tileSize: 256,
            attribution: "© Esri"
            }
        },
        layers: [
            {
            id: "esri-layer",
            type: "raster",
            source: "esri"
            }
        ]
        },
    center: startCenter,
    zoom: startZoom
  });

  map.addControl(new maplibregl.NavigationControl());
  map.addControl({
    onAdd() {
      const button = document.createElement("button");
      button.className = "maplibregl-ctrl-icon map-reset-control";
      button.type = "button";
      button.setAttribute("aria-label", "Karte zurücksetzen");
      button.title = "Karte zurücksetzen";
      button.innerHTML = "↺";
      button.addEventListener("click", () => {
        map.flyTo({ center: startCenter, zoom: startZoom });
      });

      const container = document.createElement("div");
      container.className = "maplibregl-ctrl maplibregl-ctrl-group";
      container.appendChild(button);
      return container;
    },
    onRemove() {}
  }, "top-right");

  return map;
}
