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
# ESTILOS (PC + CELULAR)
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

/* TABLA PC */
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

/* LINKS */
a {
    color: #1f77b4;
    text-decoration: underline;
}

/* TARJETAS CELULAR */
.card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
    background-color: #fafafa;
}

.card-title {
    font-weight: bold;
    margin-bottom: 6px;
}

.card-item {
    font-size: 14px;
    margin-bottom: 4px;
}

/* OCULTAR TABLA EN CELULAR */
@media (max-width: 768px) {
    .desktop-only {
        display: none;
    }
}

/* OCULTAR TARJETAS EN PC */
@media (min-width: 769px) {
    .mobile-only {
        display: none;
    }
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

    df["_search"] = (
        df.astype(str)
        .apply(lambda x: " ".join(x), axis=1)
        .str.lower()
    )

    return df

df = cargar_datos()

# =========================
# FUNCIÓN LINKS
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
# NORMALIZAR BÚSQUEDA
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
    columnas_nombres = df.columns[columnas_fijas]

    filtrado = df[df["_search"].str.contains(texto, na=False)]
    resultados = filtrado[columnas_nombres].head(10)

    if not resultados.empty:
        st.markdown(f"**Resultados encontrados:** {len(resultados)}")

        # ===== TABLA (PC)
        tabla = hacer_links(resultados)
        st.markdown(
            f"<div class='desktop-only'>{tabla.to_html(index=False, escape=False)}</div>",
            unsafe_allow_html=True
        )

        # ===== TARJETAS (CELULAR)
        st.markdown("<div class='mobile-only'>", unsafe_allow_html=True)

        for _, fila in resultados.iterrows():
            st.markdown(f"""
            <div class="card">
                <div class="card-title">{fila[columnas_nombres[0]]}</div>
                <div class="card-item"><b>{columnas_nombres[1]}:</b> {fila[columnas_nombres[1]]}</div>
                <div class="card-item"><b>{columnas_nombres[2]}:</b> {fila[columnas_nombres[2]]}</div>
                <div class="card-item"><b>{columnas_nombres[3]}:</b> {fila[columnas_nombres[3]]}</div>
                <div class="card-item"><b>{columnas_nombres[4]}:</b> {fila[columnas_nombres[4]]}</div>
                <div class="card-item"><b>{columnas_nombres[5]}:</b>
                    {fila[columnas_nombres[5]] if not str(fila[columnas_nombres[5]]).startswith("http")
                    else f"<a href='{fila[columnas_nombres[5]]}' target='_blank'>Abrir enlace</a>"}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("No se encontraron resultados")
