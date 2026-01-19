import streamlit as st
import pandas as pd
import re

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
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.markdown("<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>INVENTARIO</p>", unsafe_allow_html=True)

# =========================
# LINK CSV PUBLICADO (CORRECTO)
# =========================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRqvgoLkCTGBXrDPQgs4kIDa8YgZqk0lyMh9vJ8_IiipSRmJJN2kReZzsH8n8YCDg/pub?gid=1171023241&single=true&output=csv"

# =========================
# BOTÓN ACTUALIZAR (ANTI BUG)
# =========================
if st.button("🔄 Actualizar datos"):
    st.cache_data.clear()
    st.rerun()

# =========================
# CARGA DE DATOS (ESTABLE)
# =========================
@st.cache_data(ttl=600)
def cargar_datos():
    df = pd.read_csv(URL_CSV)

    # Limpieza
    df.columns = df.columns.str.strip()
    df = df.fillna("-")

    # Columna búsqueda
    df["_search"] = (
        df.astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
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
# NORMALIZAR BÚSQUEDA (FB)
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

    # Evita error si cambian columnas
    columnas_fijas = [i for i in columnas_fijas if i < len(df.columns)]
    columnas = df.columns[columnas_fijas]

    filtrado = df[df["_search"].str.contains(texto, na=False)]
    resultados = filtrado[columnas].head(10)

    if not resultados.empty:
        st.markdown(f"**Resultados encontrados:** {len(resultados)}")

        resultados = hacer_links(resultados)

        st.markdown(
            f"<div class='table-scroll'>{resultados.to_html(index=False, escape=False)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("No se encontraron resultados")
