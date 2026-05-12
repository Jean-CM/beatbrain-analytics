import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
from io import BytesIO

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JATune Command Center v2", layout="wide", page_icon="🚀")

# Estilo Ejecutivo
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { border: 1px solid #30363d; padding: 15px; border-radius: 10px; background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. AUTENTICACIÓN ---
client_id = st.secrets.get("SPOTIPY_CLIENT_ID")
client_secret = st.secrets.get("SPOTIPY_CLIENT_SECRET")

if not client_id or not client_secret:
    st.error("❌ No se encontraron las credenciales en los Secrets de Streamlit.")
    st.stop()

try:
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    st.error(f"⚠️ Error al configurar Spotify: {e}")
    st.stop()

# --- 2. BASE DE DATOS JATUNE ---
data_label = {
    "Artista": [
        "Jeantune", "JCSTUDIO", "JMAR", "YlegMoon", "Batytune", 
        "Jzentrix", "JironPulse", "God Herd", "JJ Legacy", "Cielaurum", 
        "QuietMetric", "AetherFocus", "ZukiPop", "LexiGo", "VYRONEX", 
        "AEROVIA", "TechMich", "KRYONEXIS"
    ],
    "Spotify_ID": [
        "5fEcz8Q0qnekHiZiBZRvKju", "3ASXkestGC7vmqDO5yCLse", "18c6Dk2b6hMLzB8cmzzrPY", 
        "75CFdTAN4KXDm49EDGYP9M", "1t3wLDYDKnbrRhell7tPEO", "3dlOSWZSXIbqHkWBPzL3SQ", 
        "3pWBw0J1CRdJIAuEz67yhe", "2rUGiDQNhoO41BZKMgRYgm", "2YbvhdJvr2ZZ1wzudZNSVR", 
        "5eEX6GcNTOyrlQIKp8Asew", "2fhCGiSMjmTsPGKs4B5AoI", "6gh5WiuhW8GrejVgEe0WGl", 
        "5Zy1nYnSiKShTBWMFeZZd", "2QCM36AO3ybRv3oSK2DhVM", "7pCE2OyAviRAYxybPadGRr", 
        "5WWodGHXJkYv35xd95wm0k", "2Ahe0ypbR1U5rPMPndhSQX", "3mm1UR6VLrbUayPoRa5RfC"
    ],
    "Autor": ["Jean C", "Jean C", "Jean C", "Angely", "Angely", "Dari", "Micha", "Jean C", "Jean C", "Angely", "Dari", "Jean C", "Jean C", "Jean C", "Jean C", "Jean C", "Micha", "Angy"],
    "Distribuidor": ["Distrokid", "Distrokid", "Ditto", "Distrokid", "Distrokid", "Distrokid", "Distrokid", "TuneCore", "Symphonic", "Ditto", "Ditto", "Ditto", "Distrokid", "Distrokid", "Distrokid", "Distrokid", "Distrokid", "Symphonic"]
}
df_label = pd.DataFrame(data_label)

# --- 3. FUNCIÓN DE EXTRACCIÓN ---
@st.cache_data(ttl=3600)
def get_full_artist_data(artist_id):
    try:
        a = sp.artist(artist_id)
        albums = sp.artist_albums(a['id'], album_type='single,album', limit=1)
        last_release = albums['items'][0]['name'] if albums['items'] else "Sin lanzamientos"
        release_date = albums['items'][0]['release_date'] if albums['items'] else "N/A"
        
        return {
            "Spotify_ID": a['id'],
            "Seguidores": a['followers']['total'],
            "Popularidad": a['popularity'],
            "Último Lanzamiento": last_release,
            "Fecha": release_date,
            "Imagen": a['images'][0]['url'] if a['images'] else None
        }
    except Exception as e:
        return {"Spotify_ID": artist_id, "Error": str(e)}

# --- 4. PROCESAMIENTO ---
with st.spinner('Actualizando métricas de JATune...'):
    results = [get_full_artist_data(sid) for sid in df_label["Spotify_ID"]]
    df_metrics = pd.DataFrame(results)
    
    # Si hay errores en la API, mostrarlos para debug
    if "Error" in df_metrics.columns:
        errores = df_metrics[df_metrics["Error"].notnull()]
        if not errores.empty and st.sidebar.checkbox("Mostrar Log de Errores"):
            st.sidebar.warning(f"Error en {len(errores)} artistas.")
            st.sidebar.write(errores[["Spotify_ID", "Error"]])

    df_final = pd.merge(df_label, df_metrics, on="Spotify_ID", how="left")

# --- 5. INTERFAZ ---
st.sidebar.title("🎹 JATune Control")
menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Auditoría", "Exportar"])

if menu == "Dashboard":
    st.title("🚀 JATune Analytics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Catálogo", len(df_final))
    c2.metric("Audiencia", f"{df_final['Seguidores'].fillna(0).sum():,}")
    c3.metric("Pop. Promedio", f"{int(df_final['Popularidad'].mean()) if 'Popularidad' in df_final else 0}%")

    st.markdown("---")
    if 'Popularidad' in df_final:
        fig = px.bar(df_final, x="Artista", y="Popularidad", color="Autor", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Auditoría":
    st.title("🔍 Auditoría de Catálogo")
    for _, row in df_final.iterrows():
        with st.expander(f"📌 {row['Artista']}"):
            col1, col2 = st.columns([1, 3])
            if row.get('Imagen'): col1.image(row['Imagen'], width=100)
            col2.write(f"**Último:** {row.get('Último Lanzamiento', 'N/A')}")
            col2.write(f"**Seguidores:** {row.get('Seguidores', 0):,}")
            col2.write(f"**ID:** `{row['Spotify_ID']}`")

elif menu == "Exportar":
    st.title("📦 Exportar Reporte")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_final.drop(columns=['Imagen'], errors='ignore').to_excel(writer, index=False)
    st.download_button("📥 Descargar Excel", output.getvalue(), "Reporte_JATune.xlsx")
