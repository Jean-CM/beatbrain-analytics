import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="BeatJATune BI", layout="wide", page_icon="📈")

# Estilo Premium
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .metric-card {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border-top: 5px solid #8D1C3E;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. GENERACIÓN DE DATOS HISTÓRICOS (Simulando la base de datos del Bot) ---
@st.cache_data
def generar_datos_bi():
    fechas = pd.date_range(start="2026-03-01", end="2026-04-01")
    artistas = ["Jeantune", "JCSTUDIO", "VYRONEX", "AEROVIA", "JMAR", "YlegMoon"]
    data = []
    for fecha in fechas:
        for artista in artistas:
            streams = pd.np.random.randint(500, 5000)
            revenue = streams * 0.0035
            data.append([fecha, artista, streams, revenue, "DistroKid", "USA"])
    return pd.DataFrame(data, columns=["Fecha", "Artista", "Plays", "Revenue", "Distribuidor", "País"])

df_historico = generar_datos_bi()

# --- 3. SIDEBAR ---
with st.sidebar:
    try: st.image("logo.png", use_container_width=True)
    except: st.title("JATune")
    st.header("BeatJATune BI")
    st.markdown("---")
    if st.button("🚀 SYNC SPOTIFY FOR ARTISTS"):
        st.warning("Iniciando Selenium Headless... buscando cambios en el DOM de Spotify.")

# --- 4. FILTROS SUPERIORES (Como en tu ejemplo) ---
st.title("🛡️ BeatJATune: Inteligencia de Negocios")

c_f1, c_f2, c_f3 = st.columns(3)
with c_f1:
    f_artista = st.multiselect("Artista", options=df_historico["Artista"].unique(), default=df_historico["Artista"].unique())
with c_f2:
    f_distro = st.multiselect("Distribuidor", options=df_historico["Distribuidor"].unique(), default="DistroKid")
with c_f3:
    f_fecha = st.date_input("Rango de Fechas", [datetime(2026,3,1), datetime(2026,4,1)])

# Filtrado
mask = (df_historico["Artista"].isin(f_artista)) & (df_historico["Fecha"].dt.date >= f_fecha[0]) & (df_historico["Fecha"].dt.date <= f_fecha[1])
df_filtered = df_historico[mask]

# --- 5. KPIs PRINCIPALES ---
total_rev = df_filtered["Revenue"].sum()
total_plays = df_filtered["Plays"].sum()
rpm = (total_rev / total_plays) * 1000 if total_plays > 0 else 0

k1, k2, k3, k4 = st.columns(4)
with k1: st.markdown(f'<div class="metric-card"><h5>Revenue Total</h5><h2>${total_rev:,.2f}</h2></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="metric-card"><h5>Plays Totales</h5><h2>{total_plays:,}</h2></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="metric-card"><h5>RPM Promedio</h5><h2>${rpm:.2f}</h2></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="metric-card"><h5>Mejor Mercado</h5><h2>USA</h2></div>', unsafe_allow_html=True)

# --- 6. GRÁFICAS DE TENDENCIA (Trend per Day) ---
st.subheader("📈 Revenue Trend por día")
df_trend = df_filtered.groupby("Fecha")["Revenue"].sum().reset_index()
fig_trend = px.line(df_trend, x="Fecha", y="Revenue", 
                    line_shape="spline", render_mode="svg")
fig_trend.update_traces(line_color='#8D1C3E', fill='tozeroy')
st.plotly_chart(fig_trend, use_container_width=True)

# --- 7. RANKINGS ---
col_r1, col_r2 = st.columns(2)

with col_r1:
    st.subheader("📊 Ranking de Artistas")
    df_art = df_filtered.groupby("Artista")[["Plays", "Revenue"]].sum().sort_values("Revenue", ascending=False)
    df_art["RPM"] = (df_art["Revenue"] / df_art["Plays"]) * 1000
    st.dataframe(df_art.style.background_gradient(cmap='Reds'), use_container_width=True)

with col_r2:
    st.subheader("🌍 Revenue por País")
    fig_pais = px.bar(df_filtered, x="País", y="Revenue", color="Artista", barmode="group")
    st.plotly_chart(fig_pais, use_container_width=True)
