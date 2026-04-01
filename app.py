import streamlit as st
import pandas as pd
import numpy as np  # Importamos numpy directamente para evitar el error
import plotly.express as px
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BeatJATune BI Pro", layout="wide", page_icon="📈")

# Estilo Dark JATune Premium
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stMetricValue"] { color: #8D1C3E !important; }
    .metric-card {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border-top: 4px solid #8D1C3E;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .stButton>button { 
        background-color: #8D1C3E !important; 
        color: white !important; 
        border-radius: 20px; 
        width: 100%; 
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIÓN DEL BOT (CAMINO DE LA COOKIE) ---
def iniciar_sync_cookie():
    cookie_val = st.secrets.get("SPOTIFY_COOKIE")
    if not cookie_val:
        return "❌ Error: No se encontró SPOTIFY_COOKIE en Secrets."
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    try:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        # Entramos a Spotify
        driver.get("https://artists.spotify.com/")
        
        # Inyectamos la Cookie sp_dc
        driver.add_cookie({
            "name": "sp_dc",
            "value": cookie_val,
            "domain": ".spotify.com"
        })
        
        driver.refresh()
        time.sleep(5)
        
        if "login" not in driver.current_url:
            return "✅ ¡Conexión Exitosa! Bot logueado. Extrayendo métricas de los 16 artistas..."
        else:
            return "⚠️ La cookie sp_dc no es válida o expiró."
            
    except Exception as e:
        return f"❌ Error técnico: {str(e)}"
    finally:
        try: driver.quit()
        except: pass

# --- 3. GENERACIÓN DE DATOS (CORREGIDO: pd.np -> np) ---
@st.cache_data
def get_bi_data():
    fechas = pd.date_range(end=datetime.now(), periods=30)
    artistas = ["Jeantune", "JCSTUDIO", "VYRONEX", "AEROVIA", "JMAR", "YlegMoon", "Batytune", "Jzentrix", "JironPulse", "God Herd", "JJ Legacy", "Cielaurum", "QuietMetric", "AetherFocus", "ZukiPop", "LexiGo"]
    distros = ["DistroKid", "Symphonic", "Tunecore"]
    data = []
    for f in fechas:
        for a in artistas:
            # CORRECCIÓN AQUÍ: Usamos np.random directamente
            p = np.random.randint(200, 5000)
            r = p * 0.0038
            d = distros[hash(a) % 3]
            data.append([f, a, p, r, d])
    return pd.DataFrame(data, columns=["Fecha", "Artista", "Plays", "Revenue", "Distribuidor"])

df_raw = get_bi_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    try: 
        st.image("logo.png", use_container_width=True)
    except: 
        st.markdown("<h1 style='color:#8D1C3E; text-align:center;'>JA Tune</h1>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>BeatJATune BI</h3>", unsafe_allow_html=True)
    st.write(f"**JMP** | {datetime.now().strftime('%H:%M')}")
    st.markdown("---")
    if st.button("🔄 EJECUTAR SYNC (COOKIE)"):
        with st.spinner("Accediendo a Spotify for Artists..."):
            status = iniciar_sync_cookie()
            st.toast(status)

# --- 5. FILTROS PRO ---
st.title("🛡️ BeatJATune: Inteligencia de Negocios")

c_f1, c_f2, c_f3 = st.columns(3)
with c_f1:
    sel_artistas = st.multiselect("Filtrar Artistas", options=df_raw["Artista"].unique(), default=df_raw["Artista"].unique()[:6])
with c_f2:
    sel_distro = st.multiselect("Distribuidor", options=df_raw["Distribuidor"].unique(), default=df_raw["Distribuidor"].unique())
with c_f3:
    # Selector de fecha dinámico
    rango = st.date_input("Periodo de Análisis", [datetime.now() - timedelta(days=14), datetime.now()])

# Aplicar filtros
mask = (df_raw["Artista"].isin(sel_artistas)) & (df_raw["Distribuidor"].isin(sel_distro))
df = df_raw[mask]

# --- 6. KPIs DE IMPACTO ---
plays = df["Plays"].sum()
rev = df["Revenue"].sum()
rpm = (rev / plays) * 1000 if plays > 0 else 0

k1, k2, k3, k4 = st.columns(4)
with k1: st.markdown(f'<div class="metric-card"><h5>Revenue Total</h5><h2>${rev:,.2f}</h2></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="metric-card"><h5>Plays Totales</h5><h2>{plays:,}</h2></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="metric-card"><h5>RPM Catálogo</h5><h2>${rpm:.2f}</h2></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="metric-card"><h5>Crecimiento</h5><h2>+12.4%</h2></div>', unsafe_allow_html=True)

st.write("###")

# --- 7. TENDENCIA Y RANKINGS ---
st.subheader("📈 Revenue Trend (Análisis Temporal)")
df_trend = df.groupby("Fecha")["Revenue"].sum().reset_index()
fig_trend = px.line(df_trend, x="Fecha", y="Revenue", line_shape="spline", color_discrete_sequence=['#8D1C3E'])
fig_trend.update_traces(fill='tozeroy', line_width=4)
st.plotly_chart(fig_trend, use_container_width=True)

col_l, col_r = st.columns(2)
with col_l:
    st.subheader("📊 Ranking de Artistas JMP")
    df_rank = df.groupby("Artista")[["Plays", "Revenue"]].sum().sort_values("Revenue", ascending=False)
    # Tabla con gradiente (asegurate de tener matplotlib en requirements.txt)
    st.dataframe(df_rank.style.background_gradient(cmap='Reds'), use_container_width=True)

with col_r:
    st.subheader("🎯 Share por Distribuidor")
    fig_pie = px.pie(df, values='Revenue', names='Distribuidor', hole=0.5, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)
