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
# CSS RESPONSIVE
# =========================
st.markdown("""
<style>
/* ----- PC ----- */
.pc {
    display: block;
}
.movil {
    display: none;
}

/* ----- CELULAR ----- */
@media (max-width: 768px) {
    .pc {
        display: none;
    }
    .movil {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }

    .movil .stButton > button {
        height: 38px;
        padding: 0 14px;
        font-size: 0.9rem;
        border-radius: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITULO PRINCIPAL
# =========================
st.markdown(
    "<h2 style='text-align:center;'>🚗 AutoRepuestos CHASI</h2>",
    unsafe_allow_html=True
)

# =====================================================
# =================== VERSION PC ======================
# =====================================================
st.markdown("<div class='pc'>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(
        "<p style='text-align:center; font-weight:600;'>INVENTARIO</p>",
        unsafe_allow_html=True
    )

with col2:
    if st.button("🔄 Actualizar datos", key="pc_refresh"):
        st.cache_data.clear()
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ================= VERSION CELULAR ===================
# =====================================================
st.markdown("<div class='movil'>", unsafe_allow_html=True)

if st.button("🔄", key="movil_refresh"):
    st.cache_data.clear()
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# CONTENIDO PRINCIPAL
# =========================
st.divider()

# Ejemplo de contenido
st.write("📦 **Listado de productos**")

data = {
    "Producto": ["Filtro de aceite", "Bujía", "Pastillas de freno"],
    "Stock": [15, 40, 22],
    "Precio": [5.50, 3.20, 18.00]
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)
