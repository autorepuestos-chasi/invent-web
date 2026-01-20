import streamlit as st
import pandas as pd
import re
import requests
from io import StringIO
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
# URL CSV (GOOGLE DRIVE PUBLICADO)
# =========================
URL_CSV = (
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRqvgoLkCTGBXrDPQgs4kIDa8YgZqk0lyMh9vJ8_IiipSRmJJN2kReZzsH8n8YCDg/pub?gid=1711514116&single=true&output=csv"
)

# =========================
# ESTILOS
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
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
# BOTÓN ACTUALIZAR + INDICADOR
# =========================
col1, col2 = st.columns([1, 4])

with col1:
    if st.button("🔄"):
        st.cache_data.clear()
        st.rerun()

with col2:
    st.caption("Actualizar datos")

# =========================
# CARGA DE DATOS ROBUSTA
# =========================
@st.cache_data(show_spinner=False)
def cargar_datos():
    try:
        r = requests.get(URL_CSV, timeout=10)

        if r.status_code != 200:
            raise ValueError("Google Drive no responde")

        df = pd.read_csv(StringIO(r.text))
        df.columns = df.columns.str.strip()

        # Columna de búsqueda segura
        df["_search"] = (
            df.astype(str)
            .fillna("")
            .agg(" ".join, axis=1)
            .str.lower()
        )

        return df, True

    except Exception:
        return None, False

df, online = cargar_datos()

# =========================
# ESTADO ONLINE / OFFLINE
# =========================
zona_ec = pytz.timezone("America/Guayaquil")
hora_actual = datetime.now(zona_ec).strftime("%H:%M:%S")

if online:
    st.success(f"🟢 Datos actualizados correctamente — {hora_actual}")
else:
    st.warning("🟡 Google Drive está sincronizando. Intenta nuevamente en unos segundos.")
    st.stop()

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
    placeholder="Ej: código, descripción o link de Facebook"
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
