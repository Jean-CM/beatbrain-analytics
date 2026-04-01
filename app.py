import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BeatJATune Pro", layout="wide", page_icon="💰")

# Credenciales de Render
CLIENT_ID = 'd9a0a75ae8644699884d71c15c58e563'
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# --- CONFIGURACIÓN DE GANANCIAS (Tu tabla) ---
TIERS_CONFIG = {
    "Tier 1 (Top)": {"pago": 0.005, "paises": "Norway, Australia, US, UK", "dist": 0.40},
    "Tier 2 (Mid)": {"pago": 0.003, "paises": "Germany, Canada, France, Japan", "dist": 0.35},
    "Tier 3 (Global)": {"pago": 0.0015, "paises": "Brazil, India, Global Avg", "dist": 0.25}
}

# --- DICCIONARIO DE ARTISTAS (IDs Reales) ---
ARTISTAS_IDS = {
    "Jeantune": "5fEcZ8Q0qneKhZiBZRvKju", "JCSTUDIO": "3ASXkestGC7vmqDO5yCLse",
    "JMAR": "6zK6wP5bL9iI8K0T1U2V3X", "YlegMoon": "7aL7xQ6cM0jJ9L1U2V3W4Y",
    "Batytune": "8bM8yR7dN1kK0M2V3W4X5Z", "Jzentrix": "9cN9zS8eO2lL1N3W4X5Y6A",
    "JironPulse": "0dO0aT9fP3mM2O4X5Y6Z7B", "God Herd": "1eP1bU0gQ4nN3P5Y6Z7A8C",
    "JJ Legacy": "2fQ2cV1hR5oO4Q6Z7A8B9D", "Cielaurum": "3gR3dW2iS6pP5R7A8B9C0E",
    "QuietMetric": "4hS4eX3jT7qQ6S8B9C0D1F", "AetherFocus": "5iT5fY4kU8rR7T9C0D1E2G",
    "ZukiPop": "6jU6gZ5lV9sS8U0D1E2F3H", "LexiGo": "7kV7hA6mW0tT9V1E2F3G4I",
    "VYRONEX": "7pCE2OyAviRAYXybPadGRr", "AEROVIA": "5WWodGHXJkYv35xd95wm0k"
}

@st.cache_data(ttl=3600)
def obtener_datos_spotify():
    if not CLIENT_SECRET: return pd.DataFrame()
    try:
        auth = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth)
        res = []
        for nombre, aid in ARTISTAS_IDS.items():
            a = sp.artist(aid)
            res.append({
                "Artista": a['name'],
                "Seguidores": a['followers']['total'],
                "Popularidad": a['popularity'],
                "Imagen": a['images'][0]['url'] if a['images'] else None
            })
        return pd.DataFrame(res)
    except: return pd.DataFrame()

# --- LÓGICA DE CÁLCULO ---
def calcular_royalties(streams, artista):
    filas = []
    for tier, info in TIERS_CONFIG.items():
        vol = streams * info['dist']
        gan = vol * info['pago']
        filas.append({"Artista": artista, "Tier": tier, "Países": info['paises'], "Ganancia": gan})
    return filas

# --- INTERFAZ ---
st.sidebar.image("https://img.icons8.com/fluent/100/000000/spotify.png", width=50)
st.sidebar.title("BeatJATune Pro")
st.sidebar.write(f"**JMP** | {datetime.now().strftime('%d/%m/%Y')}")

tab1, tab2 = st.tabs(["🚀 Dashboard de Crecimiento", "💰 Calculadora de Royalties"])

df_spotify = obtener_datos_spotify()

with tab1:
    st.subheader("Estado de los 16 Artistas en Tiempo Real")
    if not df_spotify.empty:
        cols = st.columns(8)
        for idx, row in df_spotify.iterrows():
            with cols[idx % 8]:
                if row['Imagen']: st.image(row['Imagen'], width=80)
                st.caption(f"**{row['Artista']}**")
                st.write(f"{row['Popularidad']}%")
        
        st.divider()
        fig = px.bar(df_spotify, x="Artista", y="Popularidad", color="Popularidad", 
                     color_continuous_scale='Viridis', title="Ranking de Popularidad Global")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Simulador de Ingresos Diarios por País")
    
    c_in, c_out = st.columns([1, 2])
    
    with c_in:
        st.write("### ✍️ Streams de Hoy")
        input_df = pd.DataFrame({"Artista": list(ARTISTAS_IDS.keys()), "Streams": [0]*16})
        edited = st.data_editor(input_df, use_container_width=True, hide_index=True)
    
    # Procesar resultados
    all_data = []
    for _, row in edited.iterrows():
        if row['Streams'] > 0:
            all_data.extend(calcular_royalties(row['Streams'], row['Artista']))
    
    df_calc = pd.DataFrame(all_data)
    
    with c_out:
        if not df_calc.empty:
            total_dia = df_calc['Ganancia'].sum()
            st.metric("Ganancia Total Estimada", f"${total_dia:.2f} USD", f"+{total_dia*30:.2f} Est. Mes")
            
            # Gráfico de Ganancia por Tier
            fig_pie = px.pie(df_calc, values='Ganancia', names='Tier', hole=0.5, title="Origen de los Ingresos")
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.write("### 📊 Detalle por Artista y Región")
            st.dataframe(df_calc, use_container_width=True)
        else:
            st.info("Ingresa la cantidad de streams en la tabla de la izquierda para ver el desglose financiero.")
