import streamlit as st
import pandas as pd
import re

# =========================FUNCIONA BN 
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="AutoRepuestos Chasi",
    page_icon="🚗",
    layout="centered"
)

# =========================
# ESTILOS OPTIMIZADOS CELULAR
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

table {
    width: 100% !important;
    font-size: 13px;
    border-collapse: collapse;
}

th, td {
    padding: 6px;
    text-align: left;
    word-break: break-word;
}

th {
    background-color: #f0f0f0;
}

a {
    color: #1f77b4;
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.markdown("<h2 style='text-align:center;'>🔍 Buscador de Repuestos</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AutoRepuestos Chasi</p>", unsafe_allow_html=True)

# =========================
# CARGA DE DATOS
# =========================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRqvgoLkCTGBXrDPQgs4kIDa8YgZqk0lyMh9vJ8_IiipSRmJJN2kReZzsH8n8YCDg/pub?gid=507673529&single=true&output=csv"

@st.cache_data(ttl=300)
def cargar_datos():
    df = pd.read_csv(URL_CSV)

    columnas_busqueda = df.columns.tolist()

    df["_search"] = (
        df[columnas_busqueda]
        .astype(str)
        .apply(lambda x: " ".join(x), axis=1)
        .str.lower()
    )

    return df

df = cargar_datos()

# =========================
# FUNCIÓN PARA LINKS
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
# NORMALIZAR BÚSQUEDA (URL FB)
# =========================
def normalizar_busqueda(texto):
    texto = texto.strip().lower()

    # Detectar link de Facebook Marketplace
    match = re.search(r"item/(\d+)", texto)
    if match:
        return match.group(1)  # devuelve solo el ID

    return texto

# =========================
# BUSCADOR
# =========================
busqueda = st.text_input(
    "🔎 Escribe lo que estás buscando",
    placeholder="Ej: AA23 o pega un link de Facebook"
)

# =========================
# RESULTADOS
# =========================
if busqueda:
    texto = normalizar_busqueda(busqueda)

    columnas_fijas = [0, 6, 8, 7, 2, 11]

    filtrado = df[df["_search"].str.contains(texto, na=False)]

    resultados = filtrado.iloc[:, columnas_fijas].head(10)

    if not resultados.empty:
        st.markdown(f"**Resultados encontrados:** {len(resultados)}")

        resultados = hacer_links(resultados)

        st.markdown(
            f"<div style='overflow-x:auto'>{resultados.to_html(index=False, escape=False)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("No se encontraron resultados")
