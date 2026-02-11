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

with st.spinner("⏳ Despertando la aplicación..."):
    time.sleep(0.5)

# =========================
# ESTILOS CSS (MÓVIL Y ESCRITORIO)
# =========================
st.markdown("""
<style>
/* --- ESTILOS GENERALES --- */
.block-container {
    padding-top: 2rem;
    max-width: 100%;
}
.table-scroll {
    overflow-x: auto;
}
table {
    width: 100%;
    min-width: 700px;
    font-size: 13px;
}

/* --- SOLUCIÓN PARA MÓVILES --- */
@media screen and (max-width: 800px) {
    
    /* 1. Ocultar el texto INVENTARIO */
    .ocultar-movil {
        display: none !important;
    }

    /* 2. Forzar el centrado del botón */
    /* Target a la columna que contiene el botón en móvil */
    [data-testid="stColumn"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        text-align: center !important;
    }

    /* Target al contenedor interno del botón */
    [data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* Ajuste del botón para que no se vea pegado a los bordes */
    [data-testid="stButton"] button {
        width: auto !important;
        min-width: 200px;
        margin: 10px auto !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO Y SUBTÍTULO
# =========================
st.markdown("<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>", unsafe_allow_html=True)

# Usamos la clase 'ocultar-movil' para que el CSS la detecte
st.markdown("<p class='ocultar-movil' style='text-align:center;'>INVENTARIO</p>", unsafe_allow_html=True)

if "ultima_actualizacion" in st.session_state:
    st.markdown(f"<p style='text-align:center; color:gray; font-size:0.8rem;'>🟢 Datos actualizados: {st.session_state['ultima_actualizacion']}</p>", unsafe_allow_html=True)

# =========================
# BOTÓN ACTUALIZAR
# =========================
# En escritorio, col1 ocupa el espacio y col2 pone el botón a la derecha.
# En móvil, se apilan y el CSS arriba se encarga de centrar col2.
col1, col2 = st.columns([3, 1])

with col2:
    if st.button("🔄 Actualizar datos"):
        st.cache_data.clear()
        st.rerun()

# =========================
# LÓGICA DE DATOS
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

# --- Funciones Auxiliares ---
def hacer_links(df):
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: f'<a href="{x}" target="_blank">{x}</a>'
            if isinstance(x, str) and x.startswith("http")
            else x
        )
    return df

def normalizar_busqueda(texto):
    texto = texto.strip().lower()
    match = re.search(r"item/(\d+)", texto)
    return match.group(1) if match else texto

# =========================
# BUSCADOR Y RESULTADOS
# =========================
busqueda = st.text_input("🔎 Escribe lo que estás buscando", placeholder="Ej: AA23 o link de FB")

if busqueda:
    texto = normalizar_busqueda(busqueda)
    columnas_fijas = [0, 6, 8, 7, 2, 11]
    columnas_fijas = [i for i in columnas_fijas if i < len(df.columns)]
    columnas = df.columns[columnas_fijas]

    filtrado = df[df["_search"].str.contains(texto, na=False)]
    resultados = filtrado[columnas].head(10)

    if not resultados.empty:
        st.write(f"Resultados: {len(resultados)}")
        resultados_html = hacer_links(resultados)
        st.markdown(
            f"<div class='table-scroll'>{resultados_html.to_html(index=False, escape=False)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("No se encontraron resultados")