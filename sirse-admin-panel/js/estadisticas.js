let chartTendencias, chartTiempoRespuesta, chartResolucion, chartDepartamentos;

// ================================
//   FETCH con manejo de 401
// ================================
async function authFetch(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            ...getAuthHeaders(),
            ...(options.headers || {})
        }
    });

    if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/index.html';
        return null;
    }

    return response;
}

// ================================
//   LOAD ESTADISTICAS
// ================================
async function loadEstadisticas() {
    try {
        const statsResponse = await authFetch(`${API_URL}/estadisticas/metricas-avanzadas`);
        if (!statsResponse) return;

        const stats = await statsResponse.json();

        document.getElementById('tasa-resolucion').textContent = `${stats.tasa_resolucion}%`;
        document.getElementById('tiempo-respuesta').textContent = `${stats.tiempo_respuesta}h`;
        document.getElementById('satisfaccion').textContent = `${stats.satisfaccion}/5`;
        document.getElementById('reportes-mes').textContent = stats.reportes_mes_actual;

        await loadCharts();

    } catch (error) {
        console.error("Error loading estadisticas:", error);

        document.getElementById('tasa-resolucion').textContent = "0%";
        document.getElementById('tiempo-respuesta').textContent = "0h";
        document.getElementById('satisfaccion').textContent = "0/5";
        document.getElementById('reportes-mes').textContent = "0";
    }
}

// ================================
//   LOAD CHARTS
// ================================
async function loadCharts() {
    try {
        // ------- TENDENCIAS REALES ------
        const tendenciasResponse = await authFetch(`${API_URL}/estadisticas/tendencias-semana`);
        let tendenciasData;

        if (tendenciasResponse) {
            tendenciasData = await tendenciasResponse.json();
        } else {
            tendenciasData = {
                categorias: ["Seguridad", "Robo", "Accidente", "Vandalismo"],
                semanas: ["Sem 1", "Sem 2", "Sem 3", "Sem 4"],
                datos: [
                    [30, 40, 35, 50],
                    [22, 30, 28, 31],
                    [18, 22, 26, 30],
                    [12, 18, 20, 22]
                ]
            };
        }

        const ctxTendencias = document.getElementById("chart-tendencias").getContext("2d");
        if (chartTendencias) chartTendencias.destroy();

        const colors = ["#ffd700", "#003366", "#00d084", "#ff8c00"];

        const trendDatasets = tendenciasData.categorias.map((cat, i) => ({
            label: cat,
            data: tendenciasData.datos[i],
            borderColor: colors[i],
            backgroundColor: colors[i] + "20",
            tension: 0.4
        }));

        chartTendencias = new Chart(ctxTendencias, {
            type: "line",
            data: {
                labels: tendenciasData.semanas,
                datasets: trendDatasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "bottom" } },
                scales: { y: { beginAtZero: true } }
            }
        });

        // ==============================
        //   TIEMPO DE RESPUESTA
        // ==============================
        const ctxTiempo = document.getElementById("chart-tiempo-respuesta").getContext("2d");
        if (chartTiempoRespuesta) chartTiempoRespuesta.destroy();

        chartTiempoRespuesta = new Chart(ctxTiempo, {
            type: "line",
            data: {
                labels: ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
                datasets: [{
                    label: "Horas",
                    data: [6, 4, 5, 3, 4, 2, 3],
                    borderColor: "#003366",
                    backgroundColor: "#00336620",
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });

        // ==============================
        //   TASA DE RESOLUCIÓN
        // ==============================
        const ctxResolucion = document.getElementById("chart-resolucion").getContext("2d");
        if (chartResolucion) chartResolucion.destroy();

        chartResolucion = new Chart(ctxResolucion, {
            type: "bar",
            data: {
                labels: ["Sem 1", "Sem 2", "Sem 3", "Sem 4"],
                datasets: [{
                    label: "Tasa %",
                    data: [85, 90, 88, 92],
                    backgroundColor: "#00d084",
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, max: 100 } }
            }
        });

        // ==============================
        //   DEPARTAMENTOS
        // ==============================
        const ctxDept = document.getElementById("chart-departamentos").getContext("2d");
        if (chartDepartamentos) chartDepartamentos.destroy();

        chartDepartamentos = new Chart(ctxDept, {
            type: "bar",
            data: {
                labels: [
                    "Alumbrado Público",
                    "Servicios Municipales",
                    "Parques y Jardines",
                    "Obras Públicas"
                ],
                datasets: [{
                    label: "Atendidos / Recibidos",
                    data: [245, 198, 285, 236],
                    backgroundColor: [
                        "#ffd700",
                        "#ff8c00",
                        "#00d084",
                        "#003366"
                    ],
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: true,
                plugins: { legend: { display: false } },
                scales: { x: { beginAtZero: true } }
            }
        });

    } catch (error) {
        console.error("Error loading charts:", error);
    }
}

// INIT
loadEstadisticas();
