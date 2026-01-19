import streamlit as st
import pandas as pd

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="AutoRepuestos Chasi",
    page_icon="🚗",
    layout="centered"
)

# =========================
# ESTILOS PARA CELULAR
# =========================
st.markdown("""
<style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    input {
        font-size: 18px !important;
    }
    .stDataFrame {
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.markdown(
    "<h2 style='text-align:center;'>🔍 Buscador de Repuestos</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>AutoRepuestos Chasi</p>",
    unsafe_allow_html=True
)

# =========================
# CARGA DE DATOS (DESDE DRIVE)
# =========================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRqvgoLkCTGBXrDPQgs4kIDa8YgZqk0lyMh9vJ8_IiipSRmJJN2kReZzsH8n8YCDg/pub?gid=507673529&single=true&output=csv"

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(URL_CSV)

df = cargar_datos()

# =========================
# BUSCADOR
# =========================
busqueda = st.text_input(
    "🔎 Escribe lo que estás buscando",
    placeholder="Ej: bujía, filtro, Toyota...",
)

# =========================
# RESULTADOS (TABLA FIJA)
# =========================
if busqueda:
    texto = busqueda.lower().strip()

    # Columnas fijas 
    columnas_fijas = [0, 6, 8, 7, 2, 11]

    filtrado = df[
        df.astype(str)
        .apply(lambda x: x.str.lower().str.contains(texto))
        .any(axis=1)
    ]

    resultados = filtrado.iloc[:, columnas_fijas].head(10)


    if not resultados.empty:
        st.markdown(f"**Resultados encontrados:** {len(resultados)}")
	resultados = resultados.reset_index(drop=True)
        st.table(resultados)
    else:
        st.warning("No se encontraron resultados")
