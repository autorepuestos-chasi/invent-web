import streamlit as st
import pandas as pd
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
# ESTILOS RESPONSIVE
# =========================
st.markdown("""
<style>
.main { max-width: 100%; }
table { width: 100% !important; font-size: 14px; }
th, td { padding: 6px 8px; }
th { background-color: #f2f2f2; }
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
    return pd.read_csv(URL_CSV)

df = cargar_datos()

# =========================
# SESSION STATE (DEBOUNCE)
# =========================
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()

# =========================
# BUSCADOR
# =========================
busqueda = st.text_input(
    "🔎 Escribe lo que estás buscando",
    placeholder="Ej: bujia toyota | filtro chevrolet"
)

# =========================
# DEBOUNCE (400 ms)
# =========================
now = time.time()
buscar = False

if busqueda != st.session_state.last_input:
    st.session_state.last_input = busqueda
    st.session_state.last_time = now
else:
    if now - st.session_state.last_time > 0.4:
        buscar = True

# =========================
# FUNCIÓN AND / OR
# =========================
def filtrar_and_or(df, texto):
    texto = texto.lower()

    bloques_or = [b.strip() for b in texto.split("|")]

    mask_final = pd.Series(False, index=df.index)

    for bloque in bloques_or:
        palabras_and = bloque.replace("+", " ").split()

        mask_and = pd.Series(True, index=df.index)
        for palabra in palabras_and:
            mask_and &= df.astype(str).apply(
                lambda col: col.str.lower().str.contains(palabra)
            ).any(axis=1)

        mask_final |= mask_and

    return df[mask_final]

# =========================
# RESULTADOS
# =========================
if busqueda and buscar:

    columnas_fijas = [6, 8, 7, 2, 11]  # SIN columna fantasma
    filtrado = filtrar_and_or(df, busqueda)
    resultados = filtrado.iloc[:, columnas_fijas].head(10)

    if not resultados.empty:
        st.markdown(f"**Resultados encontrados:** {len(resultados)}")
        st.markdown(resultados.to_html(index=False), unsafe_allow_html=True)
    else:
        st.warning("No se encontraron resultados")
