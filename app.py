import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BeatJATune - Inteligencia Musical", layout="wide", page_icon="📈")

# --- DISEÑO CUSTOM (CSS CORREGIDO) ---
st.markdown("""
<style>
    /* Color vino de JATune para botones y acentos */
    .stButton>button {
        background-color: #8D1C3E !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #A32A4D !important;
        transform: scale(1.05);
    }
    /* Estilo para las métricas en color vino */
    [data-testid="stMetricValue"] {
        color: #8D1C3E !important;
    }
    /* Estilo para el contenedor de ganancias */
    .ganancia-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        border-left: 10px solid #8D1C3E;
    }
</style>
""", unsafe_allow_html=True) # <-- AQUÍ ESTABA EL ERROR CORREGIDO

# --- SIDEBAR: Logotipo y Nombre ---
with st.sidebar:
    # Mostramos el logo JATune (asegúrate de que la URL sea accesible o usa el archivo local)
    st.image("https://raw.githubusercontent.com/tu_usuario/tu_repo/main/image_c61636.png", 
             caption="JATune - Music Label", use_container_width=True)
    
    st.title("BeatJATune")
    st.markdown("---")
    st.write(f"📂 **Categoría:** Catálogo JMP")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")

# --- ESTADO DE DATOS ---
if 'data_sync' not in st.session_state:
    st.session_state['data_sync'] = pd.DataFrame()

# --- INTERFAZ PRINCIPAL ---
st.title("📊 Centro de Comando JMP")
st.markdown("Gestión de activos y análisis de ingresos en tiempo real.")

tab1, tab2 = st.tabs(["🚀 Dashboard", "💰 Royalties"])

with tab1:
    col_a, col_b = st.columns([2, 1])
    with col_b:
        st.info("Activa el bot de Selenium para traer la data real de tus 16 perfiles.")
        if st.button("🤖 Iniciar Sincronización"):
            with st.spinner("Bot JMP en movimiento..."):
                # Simulación de datos para la vista
                st.session_state['data_sync'] = pd.DataFrame({
                    "Artista": ["Jeantune", "JCSTUDIO", "VYRONEX", "AEROVIA", "JMAR", "YlegMoon"],
                    "Streams": [1250, 850, 3200, 450, 980, 1100],
                    "Oyentes": [400, 310, 1200, 150, 300, 350]
                })
                st.success("✅ Sincronización BeatJATune Exitosa")
    
    with col_a:
        if not st.session_state['data_sync'].empty:
            st.dataframe(st.session_state['data_sync'], use_container_width=True)
        else:
            st.warning("⚠️ Sin datos actuales. Pulsa 'Iniciar Sincronización'.")

with tab2:
    if not st.session_state['data_sync'].empty:
        df = st.session_state['data_sync']
        total_s = df["Streams"].sum()
        
        # Cálculo basado en tus Tiers (promedio aproximado)
        ganancia = total_s * 0.0028 
        
        st.markdown(f"""
        <div class="ganancia-box">
            <h3 style="margin:0;">Ganancia Total Ayer</h3>
            <h1 style="color:#8D1C3E; margin:10px 0;">${ganancia:.2f} USD</h1>
            <p style="margin:0; color:#555;">Basado en {total_s:,} streams totales del catálogo.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Esperando sincronización para calcular ganancias...")
