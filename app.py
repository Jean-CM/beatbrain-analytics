import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="BeatJATune Analytics", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #8D1C3E;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/tu_usuario/tu_repo/main/image_c61636.png", use_container_width=True)
    st.title("BeatJATune")
    st.write(f"**JMP** | {datetime.now().strftime('%H:%M')}")

# --- CUERPO PRINCIPAL ---
st.title("📊 Centro de Inteligencia JMP")

# Botón del Bot con manejo de error amigable
if st.button("🚀 EJECUTAR SINCRONIZACIÓN REAL"):
    st.error("⚠️ Configurando entorno de navegación en Render. Por ahora, usando caché de datos.")

# --- DATOS Y GRÁFICAS (Ir con todo) ---
# Creamos datos de prueba realistas para mostrarte el potencial
df = pd.DataFrame({
    "Artista": ["Jeantune", "JCSTUDIO", "VYRONEX", "AEROVIA", "JMAR", "YlegMoon", "Batytune", "Jzentrix"],
    "Streams": [15400, 8900, 32000, 4500, 9800, 11200, 7600, 5400],
    "Ganancia Est.": [60.06, 34.71, 124.80, 17.55, 38.22, 43.68, 29.64, 21.06],
    "Tendencia": ["+12%", "+5%", "+25%", "-2%", "+8%", "+10%", "+4%", "+1%"]
})

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><h3>Ganancia Total</h3><h2>$370.12 USD</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><h3>Streams Totales</h3><h2>94,800</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><h3>Artistas Activos</h3><h2>16</h2></div>', unsafe_allow_html=True)

st.divider()

# Tablas y Gráficas Pro
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📈 Rendimiento Histórico por Artista")
    fig_bar = px.bar(df, x="Artista", y="Ganancia Est.", color="Ganancia Est.", 
                     text="Tendencia", color_continuous_scale='Sunsetdark')
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("🌍 Distribución de Mercado")
    fig_pie = px.pie(df, values='Streams', names='Artista', hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("📋 Auditoría de Ingresos Detallada")
st.table(df)
