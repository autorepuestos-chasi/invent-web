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

# =========================
# EL ÚLTIMO RECURSO: CSS ULTRA-ESPECÍFICO
# =========================
st.markdown("""
<style>
/* Estilos generales */
.block-container { padding-top: 2rem; }

/* --- SOLO PARA MÓVILES (Menos de 768px) --- */
@media screen and (max-width: 768px) {
    
    /* 1. Ocultar el texto INVENTARIO de forma absoluta */
    .solo-pc-inventario {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }

    /* 2. Forzar centrado del botón Actualizar */
    /* Rompemos el comportamiento de la columna de Streamlit */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
        display: block !important;
        text-align: center !important;
    }

    /* Centramos el botón específicamente */
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }

    .stButton > button {
        width: 80% !important; /* Más fácil de tocar en móvil */
        display: block !important;
        margin: 10px auto !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.markdown("<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>", unsafe_allow_html=True)

# Clase 'solo-pc-inventario' hará que desaparezca en móviles
st.markdown("<div class='solo-pc-inventario'><p style='text-align:center;'>INVENTARIO</p></div>", unsafe_allow_html=True)

if "ultima_actualizacion" in st.session_state:
    st.markdown(f"<p style='text-align:center; color:gray; font-size:0.8rem;'>🟢 {st.session_state['ultima_actualizacion']}</p>", unsafe_allow_html=True)

# =========================
# BOTÓN ACTUALIZAR
# =========================
# Las columnas se apilan en móvil, y el CSS de arriba centrará la segunda columna
col1, col2 = st.columns([3, 1])

with col2:
    if st.button("🔄 Actualizar datos"):
        st.cache_data.clear()
        st.rerun()

# =========================
# CARGA DE DATOS
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

# =========================
# BUSCADOR Y TABLA (RESPONSIVE)
# =========================
busqueda = st.text_input("🔎 Buscador", placeholder="Escribe aquí...")

if busqueda:
    texto = busqueda.strip().lower()
    match = re.search(r"item/(\d+)", texto)
    if match: texto = match.group(1)

    columnas_fijas = [0, 6, 8, 7, 2, 11]
    columnas_fijas = [i for i in columnas_fijas if i < len(df.columns)]
    
    filtrado = df[df["_search"].str.contains(texto, na=False)]
    
    if not filtrado.empty:
        # Usamos use_container_width para que la tabla no se rompa en móvil
        st.dataframe(
            filtrado.iloc[:, columnas_fijas].head(10), 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No encontrado")