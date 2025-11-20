document.addEventListener("DOMContentLoaded", function () {
    const mapElement = document.getElementById("map");
    if (!mapElement) {
        return;
    }

    // Crear mapa centrado en Madrid
    const map = L.map("map").setView([40.4168, -3.7038], 12);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap',
    }).addTo(map);

    const markers = [];

    function colorForPlan(plan) {
        if (plan === "premium") return "#d4af37"; // dorado
        if (plan === "standard") return "#7a8cff";
        return "#888888"; // free
    }

    function loadProfessionals() {
        fetch("/api/professionals/")
            .then(response => response.json())
            .then(data => {
                markers.forEach(m => map.removeLayer(m));
                markers.length = 0;

                data.forEach(p => {
                    const circle = L.circleMarker([p.lat, p.lng], {
                        radius: p.plan === "premium" ? 10 : 7,
                        color: colorForPlan(p.plan),
                        fillColor: colorForPlan(p.plan),
                        fillOpacity: 0.85,
                    }).addTo(map);

                    circle.bindPopup(`
                        <strong>${p.alias}</strong><br/>
                        ${p.price_from ? "Desde " + p.price_from + "€" : ""}<br/>
                        <a href="/profesional/${p.id}/">Ver perfil</a>
                    `);

                    markers.push(circle);
                });
            })
            .catch(err => {
                console.error("Error cargando profesionales:", err);
            });
    }

    loadProfessionals();
});
