import streamlit as st
import pandas as pd
import re
import os
import time

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="AutoRepuestos Chasi",
    page_icon="🚗",
    layout="centered"
)

# =========================
# ESTILOS (SCROLL RESPONSIVE)
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2.2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

/* Contenedor con scroll horizontal */
.table-scroll {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

/* Tabla */
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
st.markdown("<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>INVENTARIO</p>", unsafe_allow_html=True)
if st.button("🔄 Actualizar datos"):
    st.cache_data.clear()
    st.rerun()

# =========================
# CARGA DE DATOS (ANTI CACHE DRIVE)
# =========================
URL_BASE = "https://docs.google.com/spreadsheets/d/e/2PACX-XXXX/pub?gid=507673529&single=true&output=csv"
URL_CSV = f"{URL_BASE}&v={int(time.time() // 60)}"
CACHE_LOCAL = "cache_datos.csv"

@st.cache_data(ttl=600)
def cargar_datos():
    df = pd.read_csv(URL_BASE)

    df["_search"] = (
        df.astype(str)
        .apply(lambda x: " ".join(x), axis=1)
        .str.lower()
    )

    return df

df = cargar_datos(int(time.time() // 60))


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
# NORMALIZAR BÚSQUEDA (FACEBOOK)
# =========================
def normalizar_busqueda(texto):
    texto = texto.strip().lower()
    match = re.search(r"item/(\d+)", texto)
    if match:
        return match.group(1)
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
    columnas = df.columns[columnas_fijas]

    filtrado = df[df["_search"].str.contains(texto, na=False)]
    resultados = filtrado[columnas].head(10).fillna("-")

    if not resultados.empty:
        st.markdown(f"**Resultados encontrados:** {len(resultados)}")

        resultados = hacer_links(resultados)

        st.markdown(
            f"<div class='table-scroll'>{resultados.to_html(index=False, escape=False)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("No se encontraron resultados")
