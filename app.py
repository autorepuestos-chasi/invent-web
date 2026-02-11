import streamlit as st
import pandas as pd
import re
import time
from datetime import datetime
import pytz

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="AutoRepuestos Chasi",
    page_icon="🚗",
    layout="centered"
)

with st.spinner("⏳ Cargando aplicación..."):
    time.sleep(0.5)

# =========================
# ESTILOS CSS (MÉTODO DE ALTA PRECISIÓN)
# =========================
st.markdown("""
<style>
/* Estilos para PC */
.block-container { padding-top: 2rem; max-width: 100%; }
.table-scroll { overflow-x: auto; }
table { width: 100%; min-width: 700px; font-size: 13px; }

/* --- AJUSTES PARA MÓVIL --- */
@media screen and (max-width: 768px) {
    
    /* 1. Desaparece el texto INVENTARIO */
    .texto-inventario {
        display: none !important;
    }

    /* 2. Centrado forzado del botón */
    /* Apuntamos directamente al contenedor que creamos abajo */
    .contenedor-boton-movil {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 10px 0 !important;
    }

    /* Forzamos al componente interno de Streamlit a centrarse */
    .contenedor-boton-movil div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    /* Hacemos que el botón sea un poco más ancho para que se vea mejor en móvil */
    .contenedor-boton-movil button {
        width: 80% !important;
    }

    /* Aseguramos que la columna no lo pegue a la izquierda */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO Y SUBTÍTULO
# =========================
st.markdown("<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>", unsafe_allow_html=True)

# Este texto se ocultará gracias a la clase 'texto-inventario'
st.markdown("<p class='texto-inventario' style='text-align:center;'>INVENTARIO</p>", unsafe_allow_html=True)

if "ultima_actualizacion" in st.session_state:
    st.markdown(f"<p style='text-align:center; color:gray; font-size:0.8rem;'>🟢 Actualizado: {st.session_state['ultima_actualizacion']}</p>", unsafe_allow_html=True)

# =========================
# BOTÓN ACTUALIZAR
# =========================
col1, col2 = st.columns([3, 1])

with col2:
    # Envolvemos el botón en un DIV con nuestra clase especial
    st.markdown('<div class="contenedor-boton-movil">', unsafe_allow_html=True)
    if st.button("🔄 Actualizar datos"):
        st.cache_data.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CARGA Y LÓGICA DE DATOS
# =========================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjvIAfApdQmXKQavdfz6vYdOmR1scVPOvmW66mgpDMXjMO_EyZcLI9Ezuy8vNkpA/pub?gid=1427446213&single=true&output=csv"

@st.cache_data(ttl=18000)
def cargar_datos():
    df = pd.read_csv(URL_CSV)
    df.columns = df.columns.str.strip()
    df = df.fillna("-")
    df["_search"] = df.astype(str).agg(" ".join, axis=1).str.lower()
    zona_ec = pytz.timezone("America/Guayaquil")
    st.session_state["ultima_actualizacion"] = datetime.now(zona_ec).strftime("%d/%m/%Y %H:%M:%S")
    return df

df = cargar_datos()

def hacer_links(df):
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: f'<a href="{x}" target="_blank">{x}</a>'
            if isinstance(x, str) and x.startswith("http")
            else x
        )
    return df

# =========================
# BUSCADOR
# =========================
busqueda = st.text_input("🔎 Buscador", placeholder="Escribe aquí...")

if busqueda:
    texto = busqueda.strip().lower()
    match = re.search(r"item/(\d+)", texto)
    if match: texto = match.group(1)

    columnas_fijas = [0, 6, 8, 7, 2, 11]
    columnas_fijas = [i for i in columnas_fijas if i < len(df.columns)]
    
    filtrado = df[df["_search"].str.contains(texto, na=False)]
    resultados = filtrado[df.columns[columnas_fijas]].head(10)

    if not resultados.empty:
        st.markdown(f"**Resultados:** {len(resultados)}")
        resultados_links = hacer_links(resultados)
        st.markdown(
            f"<div class='table-scroll'>{resultados_links.to_html(index=False, escape=False)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("No encontrado")