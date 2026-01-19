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
/* Contenedor centrado */
.main {
    max-width: 100%;
}

/* Tabla responsive */
table {
    width: 100% !important;
    font-size: 14px;
    border-collapse: collapse;
}

/* Celdas */
th, td {
    padding: 6px 8px;
    text-align: left;
    word-wrap: break-word;
}

/* Encabezados */
th {
    background-color: #f2f2f2;
}

/* Links */
a {
    color: #1f77b4;
    text-decoration: underline;
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
def hacer_links(df):
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: f'<a href="{x}" target="_blank">{x}</a>'
            if isinstance(x, str) and x.startswith("http")
            else x
        )
    return df

    if not resultados.empty:
        st.markdown(f"**Resultados encontrados:** {len(resultados)}")
        st.markdown(
            resultados.to_html(index=False),
            unsafe_allow_html=True
)

    else:
        st.warning("No se encontraron resultados")
