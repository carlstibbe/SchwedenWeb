export function addMarkers(map, data, color) {

  const markers = [];

  data.forEach(loc => {

    const popup = new maplibregl.Popup()
      .setHTML(`<b>${loc.title}</b><br>${loc.text}`);

  const el = document.createElement("div");
    el.style.fontSize = "28px";
    el.style.cursor = "pointer";
    el.style.userSelect = "none";
    el.innerHTML = loc.emoji ?? "📍";

    const marker = new maplibregl.Marker({ element: el })  // ← so muss es übergeben werden!
      .setLngLat(loc.coords)
      .setPopup(popup);

    markers.push(marker);
  });

  return markers;
}
