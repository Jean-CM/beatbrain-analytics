import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BeatJATune - Inteligencia Musical", layout="wide", page_icon="📈")

# --- DISEÑO CUSTOM (CSS) para dinamismo ---
st.markdown("""
<style>
    /* Cambiar el color de acento de Streamlit (botones, sliders, etc.) al color vino de tu logo */
    :root {
        --primary-color: #8D1C3E; /* El color granate/vino de JATune */
    }
    .stButton>button {
        background-color: #8D1C3E;
        color: white;
        border-radius: 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #A32A4D;
        transform: scale(1.05);
    }
    /* Estilo para las métricas */
    div[data-testid="stMetricValue"] {
        color: #8D1C3E;
    }
</style>
""", unsafe_allow_stdio=True)

# --- SIDEBAR: Incorporación del Logo de JATune ---
# Usamos la URL directa de la imagen que me diste
url_logo_jatune = "https://files.oaiusercontent.com/file-2mN4M0zH0I8GzJ0S5K4C7P7F?se=2024-05-23T16%3A32%3A58Z&sp=r&rscc=max-age%3D604800%2C%20immutable&rscd=attachment%3B%20filename%3Db63ff134-c7ff-43b6-99ff-4ff2b7044f51.png&sig=4N3K%2BM0mY1I2j1o0R6u0I3R8p%2BQ0o2I%3D"

# Contenedor del sidebar para el logo y el nombre
with st.sidebar:
    st.image(image_12.png, use_column_width=True) # Logo dinámico arriba
    st.title("BeatJATune") # Nombre sin el "Pro"
    st.markdown("---")
    st.write(f"📂 **Categoría:** Catálogo JMP")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")

# --- ESTADO DE LA MÁQUINA (Session State) ---
if 'historico_ganancias' not in st.session_state:
    st.session_state['historico_ganancias'] = pd.DataFrame()

# --- INTERFAZ PRINCIPAL DINÁMICA ---
st.title("📊 Centro de Comando JMP")
st.markdown("Sincronización total con *Spotify for Artists* y cálculo de Royalties por país.")

tab1, tab2 = st.tabs(["🚀 Dashboard de Crecimiento", "💰 Calculadora de Royalties (Tiered)"])

with tab1:
    st.subheader("Estado de los 16 Perfiles")
    c1, c2 = st.columns([3, 1])
    with c2:
        st.info("Presiona el botón para activar el bot de Selenium.")
        if st.button("🤖 Iniciar Sincronización Directa"):
            with st.spinner("Bot JMP navegando..."):
                # Simulación para vista
                st.session_state['historico_ganancias'] = pd.DataFrame({
                    "Artista": ["Jeantune", "JCSTUDIO", "VYRONEX", "AEROVIA"],
                    "Streams": [1250, 850, 3200, 450],
                    "Oyentes Activos": [400, 310, 1200, 150]
                })
                st.success("✅ Datos sincronizados.")
    with c1:
        if not st.session_state['historico_ganancias'].empty:
            st.dataframe(st.session_state['historico_ganancias'], use_container_width=True)
        else:
            st.warning("🔄 Sincroniza los datos para ver la tabla.")

with tab2:
    st.subheader("Simulador de Ingresos Diarios por Región (Tabla Tiered)")
    if not st.session_state['historico_ganancias'].empty:
        df = st.session_state['historico_ganancias']
        total_streams = df["Streams"].sum()
        
        # Usamos tu tabla de tiers para el cálculo (promedio rápido 0.0039 T1, 0.0019 T2, 0.0009 T3)
        pago_promedio = 0.0025 # Un promedio mezclado para la vista rápida
        ganancia_estimada = total_streams * pago_promedio
        
        # Vista dinámica de resultados
        st.markdown(f"""
        <div style="background-color:#f0f2f6; border-radius:10px; padding:20px; border-left: 10px solid #8D1C3E;">
            <h3>Ganancia Total Ayer</h3>
            <h1 style="color:#8D1C3E;">${ganancia_estimada:.2f} USD</h1>
            <p>Basado en {total_streams:,} streams totales.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        # Gráfico dinámico con colores de la marca
        fig = px.bar(df, x="Artista", y="Streams", color="Streams", 
                     title="Streams por Artista", color_continuous_scale=['#8D1C3E', '#F1DBC1']) # Vino a crema
        st.plotly_chart(fig, use_container_width=True)
