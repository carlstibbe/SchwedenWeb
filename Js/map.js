export function createMap() {

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
    center: [14.391464, 58.524548],
    zoom: 6.7
  });

  map.addControl(new maplibregl.NavigationControl());

  return map;
}
