import streamlit as st
import streamlit.components.v1 as components

# Configuración básica para que use todo el ancho
st.set_page_config(layout="wide", page_title="AutoRepuestos Chasi")

# Aquí pegamos el código HTML que te pasé anteriormente
# Nota: He envuelto el código en tres comillas simples '''
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f4f4f9; margin:0; }
        .container { padding: 15px; max-width: 800px; margin: auto; background: white; border-radius: 10px; }
        h2, #subtitulo { text-align: center; }
        .header-actions { display: flex; justify-content: space-between; margin-bottom: 20px; }
        button { padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
        input { width: 100%; padding: 12px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; box-sizing: border-box; }
        .table-container { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th, td { padding: 10px; border-bottom: 1px solid #eee; text-align: left; }
        
        /* TU REQUERIMIENTO MÓVIL */
        @media screen and (max-width: 600px) {
            #subtitulo { display: none !important; }
            .header-actions { justify-content: center !important; }
            button { width: 80% !important; }
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
        <input type="text" id="searchInput" placeholder="🔎 Buscar..." oninput="filtrar()">
        <div class="table-container">
            <table>
                <thead><tr id="tableHeader"></tr></thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>
    </div>

    <script>
        const URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjvIAfApdQmXKQavdfz6vYdOmR1scVPOvmW66mgpDMXjMO_EyZcLI9Ezuy8vNkpA/pub?gid=1427446213&single=true&output=csv";
        let datos = [];
        const columnasIdx = [0, 6, 8, 7, 2, 11];

        async function cargarDatos() {
            try {
                const res = await fetch(URL_CSV);
                const text = await res.text();
                const rows = text.split('\\n').map(r => r.split(','));
                const headers = rows[0];
                datos = rows.slice(1).map(r => ({
                    vals: r,
                    searchStr: r.join(" ").toLowerCase()
                }));
                
                const thr = document.getElementById('tableHeader');
                thr.innerHTML = "";
                columnasIdx.forEach(i => {
                    const th = document.createElement('th');
                    th.innerText = headers[i] || "";
                    thr.appendChild(th);
                });
            } catch (e) { console.error(e); }
        }

        function filtrar() {
            const q = document.getElementById('searchInput').value.toLowerCase();
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = "";
            if(q.length < 2) return;

            const filtered = datos.filter(d => d.searchStr.includes(q)).slice(0, 10);
            filtered.forEach(f => {
                const tr = document.createElement('tr');
                columnasIdx.forEach(i => {
                    const td = document.createElement('td');
                    td.innerText = f.vals[i] || "-";
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
        }
        cargarDatos();
    </script>
</body>
</html>
"""

# Esta línea es la que hace la magia: incrusta el HTML en el app de Python
components.html(html_code, height=800, scrolling=True)