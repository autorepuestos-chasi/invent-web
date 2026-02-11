<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoRepuestos Chasi</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.2/papaparse.min.js"></script>
    <style>
        body { font-family: sans-serif; background-color: #f4f4f9; padding: 15px; margin: 0; }
        .container { max-width: 900px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; margin-bottom: 5px; }
        #subtitulo { text-align: center; color: #666; margin-top: 0; }
        
        .header-actions { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        
        button { padding: 10px 15px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        input { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 8px; font-size: 16px; box-sizing: border-box; }
        
        .table-container { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; min-width: 600px; }
        th, td { padding: 10px; border-bottom: 1px solid #eee; text-align: left; font-size: 13px; }
        th { background: #f8f9fa; }

        /* REQUERIMIENTOS MÓVIL */
        @media screen and (max-width: 600px) {
            #subtitulo { display: none !important; }
            .header-actions { justify-content: center !important; }
            button { width: 90% !important; font-size: 16px; }
        }
    </style>
</head>
<body>

<div class="container">
    <h2>🚗 AutoRepuestos CHASI</h2>
    <p id="subtitulo">INVENTARIO</p>

    <div class="header-actions">
        <span></span>
        <button onclick="cargarDatos()">🔄 Actualizar datos</button>
    </div>

    <input type="text" id="searchInput" placeholder="🔎 Escribe marca, modelo o código..." oninput="filtrar()">
    
    <div id="status" style="text-align:center; font-size: 12px; color: #888; margin-bottom: 10px;">Cargando base de datos...</div>

    <div class="table-container">
        <table>
            <thead><tr id="tableHeader"></tr></thead>
            <tbody id="tableBody"></tbody>
        </table>
    </div>
</div>

<script>
    const URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjvIAfApdQmXKQavdfz6vYdOmR1scVPOvmW66mgpDMXjMO_EyZcLI9Ezuy8vNkpA/pub?gid=586010588&single=true&output=csv";
    let baseDeDatos = [];
    const columnasMostrar = [0, 6, 8, 7, 2, 11]; // Índices de tus columnas

    function cargarDatos() {
        document.getElementById('status').innerText = "⏳ Actualizando...";
        
        Papa.parse(URL_CSV, {
            download: true,
            header: false, // Usamos false para manejar los índices manualmente
            complete: function(results) {
                const rows = results.data;
                if (rows.length > 0) {
                    // Guardamos los encabezados
                    const headers = rows[0];
                    renderHeaders(headers);
                    
                    // Guardamos los datos (quitando la primera fila que son encabezados)
                    baseDeDatos = rows.slice(1).map(row => {
                        return {
                            data: row,
                            searchStr: row.join(" ").toLowerCase()
                        };
                    });
                    
                    document.getElementById('status').innerText = "✅ " + baseDeDatos.length + " artículos listos.";
                }
            },
            error: function(err) {
                document.getElementById('status').innerText = "❌ Error al cargar datos.";
                console.error(err);
            }
        });
    }

    function renderHeaders(headers) {
        const tr = document.getElementById('tableHeader');
        tr.innerHTML = "";
        columnasMostrar.forEach(idx => {
            const th = document.createElement('th');
            th.innerText = headers[idx] || "Col " + idx;
            tr.appendChild(th);
        });
    }

    function filtrar() {
        const query = document.getElementById('searchInput').value.toLowerCase().trim();
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = "";

        if (query.length < 2) return;

        // Limpieza de link de Facebook
        let term = query;
        const fbMatch = query.match(/item\/(\d+)/);
        if (fbMatch) term = fbMatch[1];

        const filtrados = baseDeDatos.filter(item => item.searchStr.includes(term)).slice(0, 20);

        filtrados.forEach(item => {
            const tr = document.createElement('tr');
            columnasMostrar.forEach(idx => {
                const td = document.createElement('td');
                const valor = item.data[idx] || "-";
                
                if (valor.toString().startsWith("http")) {
                    td.innerHTML = `<a href="${valor}" target="_blank">Ver</a>`;
                } else {
                    td.innerText = valor;
                }
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }

    // Carga inicial al abrir la página
    window.onload = cargarDatos;
</script>

</body>
</html>