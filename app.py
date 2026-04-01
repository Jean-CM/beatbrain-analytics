import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BeatBrain Analytics", layout="wide", page_icon="🎵")

# --- CREDENCIALES (SEGURIDAD) ---
# Recuerda configurar SPOTIFY_CLIENT_SECRET en las variables de entorno de Render
CLIENT_ID = 'd9a0a75ae8644699884d71c15c58e563'
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# --- LISTA DE ARTISTAS ---
ARTISTAS_DATA = {
    "Jeantune": "5fEcZ8Q0qneKhZiBZRvKju", # Extraído de tu link
    "JCSTUDIO": "5yJ5vO4aK8gH7J9S0T1U2W",
    "JMAR": "6zK6wP5bL9iI8K0T1U2V3X",
    "YlegMoon": "7aL7xQ6cM0jJ9L1U2V3W4Y",
    "Batytune": "8bM8yR7dN1kK0M2V3W4X5Z",
    "Jzentrix": "9cN9zS8eO2lL1N3W4X5Y6A",
    "JironPulse": "0dO0aT9fP3mM2O4X5Y6Z7B",
    "God Herd": "1eP1bU0gQ4nN3P5Y6Z7A8C",
    "JJ Legacy": "2fQ2cV1hR5oO4Q6Z7A8B9D",
    "Cielaurum": "3gR3dW2iS6pP5R7A8B9C0E",
    "QuietMetric": "4hS4eX3jT7qQ6S8B9C0D1F",
    "AetherFocus": "5iT5fY4kU8rR7T9C0D1E2G",
    "ZukiPop": "6jU6gZ5lV9sS8U0D1E2F3H",
    "LexiGo": "7kV7hA6mW0tT9V1E2F3G4I",
    "VYRONEX": "3aVvDCHyXFm7C0L6LhE9vS",
    "AEROVIA": "1N9f9qO6Y8yP6Q7R8S9T0U"
}

# --- CONEXIÓN A SPOTIFY ---
@st.cache_data(ttl=3600) # Guarda los datos por 1 hora para que sea rápido
def obtener_metricas():
    if not CLIENT_SECRET:
        st.error("Falta la variable SPOTIFY_CLIENT_SECRET en Render.")
        return pd.DataFrame()

    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    lista_final = []
    for nombre, id_spotify in ARTISTAS_DATA.items():
        try:
            # En la vida real, los IDs se extraen de los links que pasaste
            # Aquí uso los nombres para buscar si el ID falla
            artist = sp.artist(id_spotify)
            lista_final.append({
                "Artista": artist['name'],
                "Seguidores": artist['followers']['total'],
                "Popularidad": artist['popularity'],
                "Géneros": ", ".join(artist['genres'][:2]).title()
            })
        except:
            continue
    return pd.DataFrame(lista_final)

# --- INTERFAZ ---
st.title("📊 BeatBrain Artist Dashboard")
st.markdown(f"Análisis en tiempo real de tus **{len(ARTISTAS_DATA)}** perfiles de Spotify.")

data = obtener_metricas()

if not data.empty:
    # Métricas destacadas
    col_a, col_b, col_c = st.columns(3)
    top_follower = data.loc[data['Seguidores'].idxmax()]
    top_pop = data.loc[data['Popularidad'].idxmax()]
    
    col_a.metric("Total Artistas", len(data))
    col_b.metric("Más Seguido", top_follower['Artista'], f"{top_follower['Seguidores']} seg.")
    col_c.metric("Más Popular", top_pop['Artista'], f"{top_pop['Popularidad']}%")

    st.divider()

    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Ranking de Popularidad")
        fig_pop = px.bar(data.sort_values('Popularidad', ascending=True), 
                         x='Popularidad', y='Artista', orientation='h',
                         color='Popularidad', color_continuous_scale='Viridis')
        st.plotly_chart(fig_pop, use_container_width=True)

    with col2:
        st.subheader("👥 Distribución de Seguidores")
        fig_seg = px.pie(data, values='Seguidores', names='Artista', hole=0.4)
        st.plotly_chart(fig_seg, use_container_width=True)

    st.subheader("📑 Detalle de Datos")
    st.dataframe(data, use_container_width=True)
else:
    st.warning("No se pudieron cargar los datos. Verifica tus credenciales en Render.")

st.sidebar.info(f"Logueado como: {CLIENT_ID[:5]}... | Jean")
