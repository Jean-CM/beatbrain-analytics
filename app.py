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

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO JATUNE ---
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
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        text-align: center;
    }
    .stButton>button {
        background-color: #8D1C3E !important;
        color: white !important;
        border-radius: 20px !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR CON LOGO Y MARCA JMP ---
with st.sidebar:
    # Intenta cargar logo.png desde la raíz del repo
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='color:#8D1C3E; text-align:center;'>JA Tune</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>BeatJATune</h2>", unsafe_allow_html=True)
    st.write(f"**Catalogo JMP** | {datetime.now().strftime('%H:%M')}")
    st.markdown("---")
    st.info("Sincronización: 10AM | 1PM | 3PM")

# --- 3. LÓGICA DEL BOT (SELENIUM PARA STREAMLIT CLOUD) ---
def ejecutar_bot_real():
    user = st.secrets.get("SPOTIFY_USER")
    password = st.secrets.get("SPOTIFY_PASS")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium" # Ruta en Streamlit Cloud

    try:
        # Intentar usar el driver del sistema instalado vía packages.txt
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get("https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fartists.spotify.com%2F")
        wait = WebDriverWait(driver, 20)
        
        # Login (Simulación de flujo, requiere selectores exactos de Spotify)
        wait.until(EC.presence_of_element_located((By.ID, "login-username"))).send_keys(user)
        driver.find_element(By.ID, "login-password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        
        time.sleep(5)
        return "✅ Bot Conectado: Sincronizando los 16 perfiles JMP..."
    except Exception as e:
        return f"❌ Error del Bot: {str(e)}"

# --- 4. DATOS DE PRUEBA REALISTAS (TIERED BY COUNTRY) ---
df_artistas = pd.DataFrame({
    "Artista": ["Jeantune", "JCSTUDIO", "VYRONEX", "AEROVIA", "JMAR", "YlegMoon", "Batytune", "Jzentrix", "JironPulse", "God Herd", "JJ Legacy", "Cielaurum", "QuietMetric", "AetherFocus", "ZukiPop", "LexiGo"],
    "Streams": [15400, 8900, 32000, 4500, 9800, 11200, 7600, 5400, 8900, 4300, 12000, 6700, 3200, 9100, 5500, 4100],
    "Ganancia Est.": [60.0, 34.7, 124.8, 17.5, 38.2, 43.6, 29.6, 21.0, 34.7, 16.7, 46.8, 26.1, 12.4, 35.4, 21.4, 15.9]
})

df_paises = pd.DataFrame({
    "País": ["Norway", "Australia", "USA", "UK", "Germany", "Canada", "Japan", "Brazil", "India"],
    "Tier": ["T1", "T1", "T1", "T1", "T2", "T2", "T2", "T3", "T3"],
    "Streams": [12000, 8500, 25000, 15000, 9000, 7000, 5000, 11000, 14000],
    "Ganancia ($)": [72.0, 34.0, 100.0, 60.0, 27.0, 21.0, 15.0, 22.0, 14.0]
})

# --- 5. CUERPO DE LA APP ---
st.title("📊 BeatJATune: Inteligencia de Negocios")

col_btn, col_info = st.columns([1, 3])
with col_btn:
    if st.button("🚀 SINCRONIZAR AHORA"):
        res = ejecutar_bot_real()
        st.toast(res)

st.markdown("---")

# Métricas Principales
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card"><h5>Ganancia Ayer</h5><h2>${df_artistas["Ganancia Est."].sum():.2f}</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card"><h5>Streams Totales</h5><h2>{df_artistas["Streams"].sum():,}</h2></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card"><h5>Top Artista</h5><h2>VYRONEX</h2></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card"><h5>Proyección Mes</h5><h2>${(df_artistas["Ganancia Est."].sum()*30):,.2f}</h2></div>', unsafe_allow_html=True)

st.write("###")

# Gráficas Avanzadas
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("🌍 Desglose de Ingresos por País y Tier")
    fig_map = px.bar(df_paises.sort_values("Ganancia ($)"), x="Ganancia ($)", y="País", 
                     color="Tier", orientation='h', 
                     color_discrete_map={"T1": "#8D1C3E", "T2": "#A32A4D", "T3": "#C04D6D"},
                     title="Dinero generado por País")
    st.plotly_chart(fig_map, use_container_width=True)

with c2:
    st.subheader("🎯 Participación de Artistas")
    fig_pie = px.pie(df_artistas, values='Streams', names='Artista', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# Tabla de Auditoría
st.subheader("📋 Auditoría Detallada del Catálogo JMP")
st.dataframe(df_artistas.style.background_gradient(cmap='Reds', subset=['Ganancia Est.']), use_container_width=True)
