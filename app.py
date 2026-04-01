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

# --- LISTA DE ARTISTAS DE PRUEBA (IDs VERIFICADOS) ---
ARTISTAS_DATA = {
    "VYRONEX": "7pCE2OyAviRAYXybPadGRr",
    "Jeantune": "5fEcZ8Q0qneKhZiBZRvKju",
    "JCSTUDIO": "3ASXkestGC7vmqDO5yCLse"
}

@st.cache_data(ttl=300)
def obtener_metricas():
    if not CLIENT_SECRET:
        st.error("⚠️ Error: No se encontró 'SPOTIFY_CLIENT_SECRET' en las variables de Render.")
        return pd.DataFrame()

    try:
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        lista_final = []
        for nombre, id_spotify in ARTISTAS_DATA.items():
            try:
                artista = sp.artist(id_spotify)
                lista_final.append({
                    "Artista": artista.get('name', nombre),
                    "Seguidores": artista.get('followers', {}).get('total', 0),
                    "Popularidad": artista.get('popularity', 0),
                    "Imagen": artista.get('images', [{}])[0].get('url', "")
                })
            except Exception as e:
                st.warning(f"No se pudo cargar datos de {nombre}: {e}")
                continue
                
        return pd.DataFrame(lista_final)
    except Exception as e:
        st.error(f"Error técnico general: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("📊 BeatBrain Artist Dashboard")
st.markdown("---")

data = obtener_metricas()

if not data.empty:
    st.success(f"✅ Conectado exitosamente con {len(data)} artistas.")
    
    # Mostrar tarjetas con fotos
    cols = st.columns(len(data))
    for i, row in data.iterrows():
        with cols[i]:
            if row['Imagen']:
                st.image(row['Imagen'], width=120)
            st.metric(row['Artista'], f"{row['Popularidad']}% Pop.")
            st.write(f"👥 {row['Seguidores']:,} seg.")

    st.divider()

    # Gráfico comparativo
    st.subheader("📈 Comparativa de Popularidad Actual")
    fig = px.bar(data, x='Artista', y='Popularidad', color='Popularidad', 
                 text_auto=True, color_continuous_scale='Greens',
                 labels={'Popularidad': 'Nivel de Popularidad (0-100)'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("🔄 Sincronizando con Spotify... Si esto tarda, refresca la página.")

st.sidebar.info(f"Sesión activa: **Jean**")
if st.sidebar.button('🔄 Refrescar Datos'):
    st.cache_data.clear()
