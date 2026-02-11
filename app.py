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
# EL "SUPER" CSS (SOLUCIÓN DEFINITIVA)
# =========================
st.markdown("""
<style>
/* 1. ESTILOS PARA PC (Escritorio) */
.block-container { padding-top: 2rem; }
.table-scroll { overflow-x: auto; }

/* 2. ESTILOS SOLO PARA MÓVIL (Pantallas menores a 768px) */
@media screen and (max-width: 768px) {
    
    /* Ocultar el texto INVENTARIO */
    .seccion-inventario {
        display: none !important;
    }

    /* FORZAR CENTRADO DEL BOTÓN: 
       Targeteamos el contenedor de la columna y el contenedor del botón */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        display: flex !important;
        justify-content: center !important; /* Centra horizontalmente */
        align-items: center !important;
    }

    [data-testid="stButton"] {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* Ajuste visual del botón en móvil */
    .stButton > button {
        width: 80% !important; /* Que sea un poco más ancho en móvil para el dedo */
        margin: 0 auto !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO Y SUBTÍTULO
# =========================
st.markdown("<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>", unsafe_allow_html=True)

# Envolvemos "INVENTARIO" en un div con la clase que ocultamos en móvil
st.markdown("<div class='seccion-inventario'><p style='text-align:center;'>INVENTARIO</p></div>", unsafe_allow_html=True)

if "ultima_actualizacion" in st.session_state:
    st.caption(f"🟢 Datos actualizados: {st.session_state['ultima_actualizacion']}")

# =========================
# BOTÓN ACTUALIZAR
# =========================
# En PC esto mantiene el botón a la derecha. En móvil se apila y se centra.
col1, col2 = st.columns([3, 1])

with col2:
    if st.button("🔄 Actualizar datos"):
        st.cache_data.clear()
        st.rerun()

# =========================
# CARGA DE DATOS (MANTENIENDO TU LÓGICA)
# =========================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjvIAfApdQmXKQavdfz6vYdOmR1scVPOvmW66mgpDMXjMO_EyZcLI9Ezuy8vNkpA/pub?gid=1427446213&single=true&output=csv"

@st.cache_data(ttl=18000)
def cargar_datos():
    try:
        df = pd.read_csv(URL_CSV)
        df.columns = df.columns.str.strip()
        df = df.fillna("-")
        df["_search"] = df.astype(str).agg(" ".join, axis=1).str.lower()
        
        zona_ec = pytz.timezone("America/Guayaquil")
        st.session_state["ultima_actualizacion"] = datetime.now(zona_ec).strftime("%d/%m/%Y %H:%M:%S")
        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

# --- Buscador ---
busqueda = st.text_input("🔎 Escribe lo que estás buscando", placeholder="Ej: AA23")

if busqueda:
    texto = busqueda.strip().lower()
    # Si es link de Facebook, extraer ID
    match = re.search(r"item/(\d+)", texto)
    if match: texto = match.group(1)

    columnas_fijas = [0, 6, 8, 7, 2, 11]
    columnas_fijas = [i for i in columnas_fijas if i < len(df.columns)]
    
    filtrado = df[df["_search"].str.contains(texto, na=False)]
    
    if not filtrado.empty:
        # Aquí puedes agregar la función hacer_links si la necesitas
        st.dataframe(filtrado.iloc[:, columnas_fijas].head(10), use_container_width=True)
    else:
        st.warning("No se encontraron resultados")