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

/* Tabla limpia y centrada */
table {
    width: 100% !important;
    font-size: 13px;
    border-collapse: collapse;
}

/* Celdas */
th, td {
    padding: 6px;
    text-align: left;
    word-break: break-word;
}

/* Encabezados */
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
st.markdown(
    "<h2 style='text-align:center;'>🔍 Buscador de Repuestos</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>AutoRepuestos Chasi</p>",
    unsafe_allow_html=True
)

# =========================
# CARGA DE DATOS
# =========================
URL_CSV = "aqui la url"

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(URL_CSV)

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
# BUSCADOR
# =========================
busqueda = st.text_input(
    "🔎 Escribe lo que estás buscando",
    placeholder="Ej: bujía, filtro, Toyota..."
)

# =========================
# RESULTADOS (TABLA HTML FIJA)
# =========================
if busqueda:
    texto = busqueda.lower().strip()

    # Columnas fijas (SIN columna 0)
    columnas_fijas = [6, 8, 7, 2, 11]

    filtrado = df[
        df.astype(str)
        .apply(lambda x: x.str.lower().str.contains(texto))
        .any(axis=1)
    ]

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
