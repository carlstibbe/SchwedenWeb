export function addMarkers(map, data, color) {

  const markers = [];

  data.forEach(loc => {

  const el = document.createElement("div");
    el.style.fontSize = "28px";
    el.style.cursor = "pointer";
    el.style.userSelect = "none";
    el.innerHTML = loc.emoji ?? "📍";

    const marker = new maplibregl.Marker({ element: el })  // ← so muss es übergeben werden!
      .setLngLat(loc.coords);

    el.addEventListener("click", () => {
      const isMobile = window.matchMedia("(max-width: 768px)").matches;

      map.flyTo({
        center: loc.coords,
        zoom: 12
      });

      if (isMobile) {
        map.once("moveend", () => {
          map.panBy([0, -map.getContainer().clientHeight * 0.25], { duration: 400 });
        });
      }

      const details = document.getElementById("map-details");
      const content = document.getElementById("map-details-content");

      if (!details || !content) return;

      content.innerHTML = `
        ${loc.image ? `<img src="${loc.image}" alt="${loc.title}" />` : ""}
        <h3>${loc.title}</h3>
        <p>${loc.text}</p>
      `;
      details.classList.add("is-visible");
    });

    markers.push(marker);
  });

  return markers;
}
