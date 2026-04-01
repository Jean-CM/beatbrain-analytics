import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE CREDENCIALES (Usa los de tu imagen) ---
import os
CLIENT_ID = 'd9a0a75ae8644699884d71c15c58e563'
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') # Haz clic en "View client secret" en tu panel

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --- LISTA DE TUS ARTISTAS (IDs de Spotify) ---
# Puedes obtener el ID desde la URL de cada artista en Spotify
artist_ids = [
    'ID_AEROVIA', 'ID_VYRONEX', 'ID_LEXIGO', 'ID_JIRONPULSE'
]

st.set_page_config(page_title="BeatBrain Analytics", layout="wide")
st.title("📊 BeatBrain Artist Dashboard")
st.sidebar.header("Configuración")

def get_artist_data(ids):
    data = []
    for a_id in ids:
        try:
            artist = sp.artist(a_id)
            data.append({
                "Nombre": artist['name'],
                "Seguidores": artist['followers']['total'],
                "Popularidad": artist['popularity'],
                "Géneros": ", ".join(artist['genres'])
            })
        except:
            continue
    return pd.DataFrame(data)

# --- INTERFAZ DE USUARIO ---
if st.sidebar.button('Actualizar Datos'):
    with st.spinner('Conectando con Spotify...'):
        df = get_artist_data(artist_ids)
        st.session_state['df'] = df

if 'df' in st.session_state:
    df = st.session_state['df']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Crecimiento de Seguidores")
        fig_seg = px.bar(df, x="Nombre", y="Seguidores", color="Nombre", text_auto=True)
        st.plotly_chart(fig_seg, use_container_width=True)
        
    with col2:
        st.subheader("Índice de Popularidad (0-100)")
        fig_pop = px.line(df, x="Nombre", y="Popularidad", markers=True)
        st.plotly_chart(fig_pop, use_container_width=True)

    st.subheader("Detalle General")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Presiona 'Actualizar Datos' en la barra lateral para comenzar.")
