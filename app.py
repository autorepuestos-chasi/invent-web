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
# ESTILOS (MÓVIL + DESKTOP)
# =========================
st.markdown("""
<style>
.main {
    max-width: 100%;
    padding: 0.5rem;
}

table {
    width: 100% !important;
    font-size: 14px;
    border-collapse: collapse;
}

th, td {
    padding: 6px 8px;
    text-align: left;
    white-space: normal;
}

th {
    background-color: #f2f2f2;
}

a {
    color: #1f77b4;
    text-decoration: underline;
}

@media (max-width: 600px) {
    table {
        font-size: 12px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.markdown("<h3 style='text-align:center;'>🔍 Buscador de Repuestos</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AutoRepuestos Chasi</p>", unsafe_allow_html=True)

# =========================
# CARGA DE DATOS (CSV DRIVE)
# =========================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRqvgoLkCTGBXrDPQgs4kIDa8YgZqk0lyMh9vJ8_IiipSRmJJN2kReZzsH8n8YCDg/pub?gid=507673529&single=true&output=csv"

@st.cache_data(ttl=300)
def cargar_datos(url):
    return pd.read_csv(url)

df = cargar_datos(URL_CSV)

# =========================
# TEXTO UNIFICADO (RÁPIDO)
# =========================
@st.cache_data(ttl=300)
def preparar_texto_busqueda(df):
    return df.astype(str).agg(" ".join, axis=1).str.lower()

texto_busqueda = preparar_texto_busqueda(df)

# =========================
# BUSCADOR
# =========================
busqueda = st.text_input(
    "🔎 Escribe lo que estás buscando",
    placeholder="Ej: bujía toyota | filtro + chevrolet",
)

# =========================
# FILTRO AND / OR
# =========================
def filtrar_and_or(texto_total, texto):
    texto = texto.lower().strip()

    bloques_or = [b.strip() for b in texto.split("|")]
    mask_final = pd.Series(False, index=texto_total.index)

    for bloque in bloques_or:
        palabras_and = bloque.replace("+", " ").split()
        mask_and = pd.Series(True, index=texto_total.index)

        for palabra in palabras_and:
            mask_and &= texto_total.str.contains(palabra)

        mask_final |= mask_and

    return mask_final

# =========================
# RESULTADOS
# =========================
if busqueda:
    columnas_fijas = [0, 6, 8, 7, 2, 11]  # A, G, I, H, C, L

    mask = filtrar_and_or(texto_busqueda, busqueda)
    resultados = df.loc[mask, df.columns[columnas_fijas]].head(10)

    if not resultados.empty:
        st.markdown(f"**Resultados encontrados:** {len(resultados)}")
        st.markdown(
            resultados.to_html(index=False, escape=False),
            unsafe_allow_html=True
        )
    else:
        st.warning("No se encontraron resultados")
