export function addMarkers(map, data, color) {

  const markers = [];

  data.forEach(loc => {

    const popup = new maplibregl.Popup()
      .setHTML(`<b>${loc.title}</b><br>${loc.text}`);

    const el = document.createElement("div");
    el.style.cursor = "pointer";
    el.innerHTML = `
      <svg width="32" height="42" viewBox="0 0 32 42" xmlns="http://www.w3.org/2000/svg">
        <path d="M16 0 C7.16 0 0 7.16 0 16 C0 28 16 42 16 42 C16 42 32 28 32 16 C32 7.16 24.84 0 16 0 Z"
              fill="${color}" stroke="white" stroke-width="1.5"/>
        <circle cx="16" cy="15" r="6" fill="white"/>
      </svg>`;

    const marker = new maplibregl.Marker({ element: el })  // ← so muss es übergeben werden!
      .setLngLat(loc.coords)
      .setPopup(popup);

    markers.push(marker);
  });

  return markers;
}
