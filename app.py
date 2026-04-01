import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="BeatJATune JMP Pro", layout="wide", page_icon="📈")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1a1c24; }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #8D1C3E;
        text-align: center;
    }
    .stButton>button { background-color: #8D1C3E !important; color: white !important; border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='color:#8D1C3E; text-align:center;'>JA Tune</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>BeatJATune</h2>", unsafe_allow_html=True)
    st.write(f"**Catálogo JMP** | {datetime.now().strftime('%H:%M')}")
    st.markdown("---")
    if st.button("🚀 SINCRONIZAR AHORA"):
        st.toast("Bot iniciado... verificando perfiles.")

# --- 3. DATOS BASE ---
df_artistas = pd.DataFrame({
    "Artista": ["Jeantune", "JCSTUDIO", "VYRONEX", "AEROVIA", "JMAR", "YlegMoon", "Batytune", "Jzentrix", "JironPulse", "God Herd", "JJ Legacy", "Cielaurum", "QuietMetric", "AetherFocus", "ZukiPop", "LexiGo"],
    "Mes": ["Abril", "Marzo", "Abril", "Abril", "Marzo", "Abril", "Marzo", "Abril", "Marzo", "Abril", "Marzo", "Abril", "Marzo", "Abril", "Marzo", "Abril"],
    "Streams": [15400, 8900, 32000, 4500, 9800, 11200, 7600, 5400, 8900, 4300, 12000, 6700, 3200, 9100, 5500, 4100],
    "Ganancia Est.": [60.0, 34.7, 124.8, 17.5, 38.2, 43.6, 29.6, 21.0, 34.7, 16.7, 46.8, 26.1, 12.4, 35.4, 21.4, 15.9]
})

# --- 4. FILTROS (NUEVO) ---
st.title("📊 BeatJATune: Inteligencia de Negocios")

col_f1, col_f2 = st.columns(2)
with col_f1:
    filtro_mes = st.multiselect("📅 Seleccionar Periodo (Mes):", options=["Marzo", "Abril"], default=["Marzo", "Abril"])
with col_f2:
    filtro_artista = st.multiselect("🎤 Seleccionar Artista:", options=df_artistas["Artista"].unique(), default=df_artistas["Artista"].unique())

# Aplicar Filtros
df_filtrado = df_artistas[(df_artistas["Mes"].isin(filtro_mes)) & (df_artistas["Artista"].isin(filtro_artista))]

# --- 5. MÉTRICAS DINÁMICAS ---
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card"><h5>Ganancia Periodo</h5><h2>${df_filtrado["Ganancia Est."].sum():.2f}</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card"><h5>Streams Totales</h5><h2>{df_filtrado["Streams"].sum():,}</h2></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card"><h5>Artistas Filtrados</h5><h2>{len(df_filtrado)}</h2></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card"><h5>Proyección Mes</h5><h2>${(df_filtrado["Ganancia Est."].sum()*1.2):,.2f}</h2></div>', unsafe_allow_html=True)

st.write("###")

# --- 6. GRÁFICAS ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("🌍 Desglose de Streams")
    fig_bar = px.bar(df_filtrado.sort_values("Streams"), x="Streams", y="Artista", 
                     orientation='h', color="Streams", 
                     color_continuous_scale=['#4d0d1f', '#8D1C3E', '#ff4d7d'],
                     title="Rendimiento por Artista Seleccionado")
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("🎯 Cuota de Mercado")
    fig_pie = px.pie(df_filtrado, values='Streams', names='Artista', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# --- 7. TABLA DE AUDITORÍA (SOLUCIÓN AL ERROR) ---
st.subheader("📋 Auditoría Detallada del Catálogo JMP")

if not df_filtrado.empty:
    # Mostramos la tabla con el gradiente (requiere matplotlib en requirements.txt)
    st.dataframe(
        df_filtrado.style.background_gradient(cmap='Reds', subset=['Ganancia Est.']), 
        use_container_width=True
    )
else:
    st.warning("No hay datos para los filtros seleccionados.")
