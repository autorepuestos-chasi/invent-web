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
# CSS - EL "MARTILLO" DEFINITIVO
# =========================
st.markdown("""
<style>
/* --- ESTILOS GENERALES --- */
.block-container { padding-top: 2rem; }
.table-scroll { overflow-x: auto; }

/* --- ESTILO PARA PC (Por defecto) --- */
.contenedor-cabecera {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 10px;
}

/* --- ESTILO PARA MÓVIL --- */
@media screen and (max-width: 768px) {
    /* 1. Suprimir el texto INVENTARIO */
    #texto-inventario {
        display: none !important;
    }

    /* 2. Forzar que el contenedor del botón ocupe todo el ancho y se centre */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    /* 3. Centrar el botón específicamente */
    .stButton > button {
        width: 85% !important;
        margin: 0 auto !important;
        display: block !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.markdown("<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>", unsafe_allow_html=True)

# Usamos un ID único para el texto INVENTARIO para que el CSS lo encuentre sí o sí
st.markdown("<div id='texto-inventario'><p style='text-align:center;'>INVENTARIO</p></div>", unsafe_allow_html=True)

if "ultima_actualizacion" in st.session_state:
    st.markdown(f"<p style='text-align:center; color:gray; font-size:0.8rem;'>🟢 {st.session_state['ultima_actualizacion']}</p>", unsafe_allow_html=True)

# =========================
# BOTÓN ACTUALIZAR (SIN COLUMNAS PARA EVITAR ERRORES)
# =========================
# En lugar de usar st.columns, dejamos que Streamlit lo ponga en su flujo natural
# y nuestro CSS se encarga de centrarlo si detecta un móvil.
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
# BUSCADOR Y RESULTADOS
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
        st.dataframe(
            filtrado.iloc[:, columnas_fijas].head(10), 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No encontrado")