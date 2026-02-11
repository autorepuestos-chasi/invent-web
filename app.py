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

with st.spinner("⏳ Despertando la aplicación y cargando datos..."):
    time.sleep(0.8)

# =========================
# ESTILOS (RESPONSIVE)
# =========================
st.markdown("""
<style>

/* Layout general */
.block-container {
    padding-top: 2.2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

/* Tabla responsive */
.table-scroll {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

table {
    width: 100%;
    min-width: 720px;
    font-size: 13px;
    border-collapse: collapse;
}

th, td {
    padding: 6px 8px;
    text-align: left;
    white-space: nowrap;
}

th {
    background-color: #f0f0f0;
}

a {
    color: #1f77b4;
    text-decoration: underline;
}

/* ===== VISIBILIDAD POR DISPOSITIVO ===== */
.solo-movil {
    display: none;
}

.solo-pc {
    display: block;
}

/* ===== SOLO CELULAR ===== */
@media (max-width: 768px) {

    .solo-pc {
        display: none;
    }

    .solo-movil {
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }

    .solo-movil .stButton > button {
        height: 38px;
        padding: 0 14px;
        font-size: 0.9rem;
        border-radius: 20px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO + BOTÓN (RESPONSIVE)
# =========================
st.markdown("<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>", unsafe_allow_html=True)

# Contenedor común
st.markdown('<div>', unsafe_allow_html=True)

# TEXTO SOLO PC
st.markdown(
    "<p class='solo-pc' style='text-align:center;'>INVENTARIO</p>",
    unsafe_allow_html=True
)

# BOTÓN SOLO MÓVIL
st.markdown('<div class="solo-movil">', unsafe_allow_html=True)
if st.button("🔄 Actualizar datos"):
    st.cache_data.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ESTADO DE DATOS
# =========================
if "ultima_actualizacion" in st.session_state:
    st.caption(f"🟢 Datos actualizados: {st.session_state['ultima_actualizacion']}")

# =========================
# LINK CSV
# =========================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjvIAfApdQmXKQavdfz6vYdOmR1scVPOvmW66mgpDMXjMO_EyZcLI9Ezuy8vNkpA/pub?gid=586010588&single=true&output=csv"

# =========================
# CARGA DE DATOS
# =========================
@st.cache_data(ttl=18000)
def cargar_datos():
    df = pd.read_csv(URL_CSV)

    df.columns = df.columns.str.strip()
    df = df.fillna("-")

    df["_search"] = (
        df.astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
    )

    zona_ec = pytz.timezone("America/Guayaquil")
    st.session_state["ultima_actualizacion"] = (
        datetime.now(zona_ec).strftime("%d/%m/%Y %H:%M:%S")
    )

    return df

df = cargar_datos()

# =========================
# LINKS CLICKEABLES
# =========================
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
# NORMALIZAR BÚSQUEDA
# =========================
def normalizar_busqueda(texto):
    texto = texto.strip().lower()
    match = re.search(r"item/(\d+)", texto)
    if match:
