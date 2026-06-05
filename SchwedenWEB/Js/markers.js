export function addMarkers(map, data, color) {

  const markers = [];

  data.forEach(loc => {

  const popup = new maplibregl.Popup()
    .setHTML(`
      ${loc.image ? `<img src="${loc.image}" style="width:200px; border-radius:8px; margin-bottom:6px;"/>` : ""}
      <b>${loc.title}</b><br>${loc.text}
    `);

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
