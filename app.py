import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BeatBrain Analytics", layout="wide", page_icon="🎵")

# --- CREDENCIALES (SEGURIDAD) ---
CLIENT_ID = 'd9a0a75ae8644699884d71c15c58e563'
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# --- LISTA DE ARTISTAS REALES (IDs VERIFICADOS) ---
ARTISTAS_DATA = {
    "VYRONEX": "7pCE2OyAviRAYXybPadGRr",
    "AEROVIA": "5WWodGHXJkYv35xd95wm0k"
}

# --- CONEXIÓN A SPOTIFY ---
@st.cache_data(ttl=300) # Refresco cada 5 min para pruebas
def obtener_metricas():
    if not CLIENT_SECRET:
        st.error("⚠️ Error: Falta la variable 'SPOTIFY_CLIENT_SECRET' en Render.")
        return pd.DataFrame()

    try:
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        lista_final = []
        for nombre, id_spotify in ARTISTAS_DATA.items():
            artist = sp.artist(id_spotify)
            lista_final.append({
                "Artista": artist['name'],
                "Seguidores": artist['followers']['total'],
                "Popularidad": artist['popularity'],
                "Imagen": artist['images'][0]['url'] if artist['images'] else ""
            })
        return pd.DataFrame(lista_final)
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("📊 BeatBrain Artist Dashboard")

data = obtener_metricas()

if not data.empty:
    # Mostrar tarjetas con fotos de perfil
    cols = st.columns(len(data))
    for i, row in data.iterrows():
        with cols[i]:
            if row['Imagen']:
                st.image(row['Imagen'], width=100)
            st.metric(row['Artista'], f"{row['Popularidad']}% Pop.")
            st.caption(f"👥 {row['Seguidores']} seguidores")

    st.divider()

    # Gráfico de Popularidad
    st.subheader("📈 Comparativa de Popularidad")
    fig = px.bar(data, x='Artista', y='Popularidad', color='Artista', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Esperando datos de Spotify... Verifica que los IDs sean correctos.")

st.sidebar.success(f"Conectado como: Jean")
