import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px

# Configuración de página con look "High-Tech"
st.set_page_config(page_title="JATune Command Center", layout="wide", page_icon="🚀")

# Estilo Ejecutivo Personalizado
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { border: 1px solid #4d4d4d; padding: 10px; border-radius: 5px; background-color: #161b22; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3137,#0e1117); }
    </style>
    """, unsafe_allow_html=True)

# --- 1. AUTENTICACIÓN ---
try:
    client_id = st.secrets["d9a0a75ae8644699884d71c15c58e563"]
    client_secret = st.secrets["a45b08ed2d544142a6b7b18a48e06b08"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    st.error("⚠️ Error: Configura las credenciales en los Secrets de Streamlit.")
    st.stop()

# --- 2. BASE DE DATOS DEL SELLO JATUNE ---
data_label = {
    "Artista": ["Jeantune", "JCSTUDIO", "JMAR", "YlegMoon", "Batytune", "Jzentrix", "JironPulse", "God Herd", "JJ Legacy", "Cielaurum", "QuietMetric", "AetherFocus", "ZukiPop", "LexiGo", "VYRONEX", "AEROVIA"],
    "Autor": ["Jean C", "Jean C", "Jean C", "Angely", "Angely", "Dari", "Micha", "Jean C", "Jean C", "Angely", "Dari", "Jean C", "Jean C", "Jean C", "Jean C", "Jean C"],
    "Distribuidor": ["Distrokid", "Distrokid", "Ditto", "Distrokid", "Distrokid", "Distrokid", "Distrokid", "TuneCore", "Symphonic", "Ditto", "Ditto", "Ditto", "Distrokid", "Distrokid", "Distrokid", "Distrokid"]
}
df_label = pd.DataFrame(data_label)

# --- 3. FUNCIONES DE APOYO ---
@st.cache_data(ttl=3600)
def buscar_datos_spotify(nombre_artista):
    """Busca al artista en Spotify y extrae métricas actuales."""
    try:
        resultado = sp.search(q=f'artist:{nombre_artista}', type='artist', limit=1)
        if resultado['artists']['items']:
            a = resultado['artists']['items'][0]
            return {
                "Spotify_ID": a['id'],
                "Seguidores": a['followers']['total'],
                "Popularidad": a['popularity'],
                "Link": a['external_urls']['spotify'],
                "Imagen": a['images'][0]['url'] if a['images'] else None
            }
    except:
        return None
    return None

# --- 4. INTERFAZ PRINCIPAL ---
st.title("🎵 JATune Executive Dashboard")
st.sidebar.image("https://img.icons8.com/fluency/96/music-record.png", width=80)
st.sidebar.title("Navegación")
menu = st.sidebar.radio("Ir a:", ["Vista General", "Métricas Spotify", "Auditoría de Distribución", "Generador de Playlists"])

# Lógica de Datos: Enriquecer DataFrame con Spotify
with st.spinner('Actualizando métricas desde Spotify...'):
    metrics = []
    for art in df_label["Artista"]:
        res = buscar_datos_spotify(art)
        metrics.append(res if res else {"Spotify_ID": "N/A", "Seguidores": 0, "Popularidad": 0, "Link": "#", "Imagen": None})
    
    df_metrics = pd.DataFrame(metrics)
    df_final = pd.concat([df_label, df_metrics], axis=1)

# --- MÓDULO 1: VISTA GENERAL ---
if menu == "Vista General":
    st.subheader("📋 Resumen del Catálogo JATune")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Artistas", len(df_final))
    col2.metric("Total Seguidores", f"{df_final['Seguidores'].sum():,}")
    col3.metric("Distribuidora Principal", df_final['Distribuidor'].mode()[0])

    st.dataframe(df_final[["Artista", "Autor", "Distribuidor", "Popularidad", "Seguidores"]], use_container_width=True)

# --- MÓDULO 2: MÉTRICAS SPOTIFY ---
elif menu == "Métricas Spotify":
    st.subheader("📈 Rendimiento en Tiempo Real")
    
    fig = px.bar(df_final, x='Artista', y='Popularidad', color='Autor',
                 hover_data=['Seguidores'], title="Popularidad por Artista y Autor",
                 template="plotly_dark", barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Top Artistas por Audiencia")
    top_df = df_final.nlargest(5, 'Seguidores')
    for _, row in top_df.iterrows():
        cols = st.columns([1, 4])
        if row['Imagen']: cols[0].image(row['Imagen'], width=60)
        cols[1].write(f"**{row['Artista']}** | {row['Seguidores']:,} seguidores")

# --- MÓDULO 3: AUDITORÍA DE DISTRIBUCIÓN ---
elif menu == "Auditoría de Distribución":
    st.subheader("📦 Control de Distribuidoras")
    dist_choice = st.selectbox("Filtrar por Distribuidora", df_final['Distribuidor'].unique())
    filtered_dist = df_final[df_final['Distribuidor'] == dist_choice]
    st.table(filtered_dist[["Artista", "Autor", "Spotify_ID"]])

# --- MÓDULO 4: GENERADOR DE PLAYLISTS ---
elif menu == "Generador de Playlists":
    st.subheader("🪄 Creador Inteligente")
    st.write("Selecciona un autor para crear una playlist con sus mejores tracks.")
    autor_sel = st.selectbox("Seleccionar Autor", df_final['Autor'].unique())
    
    if st.button(f"Generar Selección para {autor_sel}"):
        artistas_autor = df_final[df_final['Autor'] == autor_sel]['Artista'].tolist()
        st.success(f"Analizando tracks para: {', '.join(artistas_autor)}")
        st.info("Función de creación directa en Spotify: Desbloqueada con User Token (OAuth).")
