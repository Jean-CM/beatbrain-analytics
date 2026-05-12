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

sp = None
if client_id and client_secret:
    try:
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")

# --- 2. BASE DE DATOS JATUNE ---
data_label = {
    "Artista": ["Jeantune", "JCSTUDIO", "JMAR", "YlegMoon", "Batytune", "Jzentrix", "JironPulse", "God Herd", "JJ Legacy", "Cielaurum", "QuietMetric", "AetherFocus", "ZukiPop", "LexiGo", "VYRONEX", "AEROVIA", "TechMich", "KRYONEXIS"],
    "Spotify_ID": ["5fEcz8Q0qnekHiZiBZRvKju", "3ASXkestGC7vmqDO5yCLse", "18c6Dk2b6hMLzB8cmzzrPY", "75CFdTAN4KXDm49EDGYP9M", "1t3wLDYDKnbrRhell7tPEO", "3dlOSWZSXIbqHkWBPzL3SQ", "3pWBw0J1CRdJIAuEz67yhe", "2rUGiDQNhoO41BZKMgRYgm", "2YbvhdJvr2ZZ1wzudZNSVR", "5eEX6GcNTOyrlQIKp8Asew", "2fhCGiSMjmTsPGKs4B5AoI", "6gh5WiuhW8GrejVgEe0WGl", "5Zy1nYnSiKShTBWMFeZZd", "2QCM36AO3ybRv3oSK2DhVM", "7pCE2OyAviRAYxybPadGRr", "5WWodGHXJkYv35xd95wm0k", "2Ahe0ypbR1U5rPMPndhSQX", "3mm1UR6VLrbUayPoRa5RfC"],
    "Autor": ["Jean C", "Jean C", "Jean C", "Angely", "Angely", "Dari", "Micha", "Jean C", "Jean C", "Angely", "Dari", "Jean C", "Jean C", "Jean C", "Jean C", "Jean C", "Micha", "Angy"],
    "Distribuidor": ["Distrokid", "Distrokid", "Ditto", "Distrokid", "Distrokid", "Distrokid", "Distrokid", "TuneCore", "Symphonic", "Ditto", "Ditto", "Ditto", "Distrokid", "Distrokid", "Distrokid", "Distrokid", "Distrokid", "Symphonic"]
}
df_final = pd.DataFrame(data_label)

# Inicializar columnas para evitar KeyError
for col in ["Seguidores", "Popularidad", "Último Lanzamiento", "Fecha", "Imagen"]:
    df_final[col] = 0 if col in ["Seguidores", "Popularidad"] else "N/A"

# --- 3. EXTRACCIÓN ---
if sp:
    with st.spinner('Sincronizando con Spotify...'):
        for i, row in df_final.iterrows():
            try:
                a = sp.artist(row['Spotify_ID'])
                df_final.at[i, 'Seguidores'] = a['followers']['total']
                df_final.at[i, 'Popularidad'] = a['popularity']
                df_final.at[i, 'Imagen'] = a['images'][0]['url'] if a['images'] else None
                
                albums = sp.artist_albums(row['Spotify_ID'], album_type='single,album', limit=1)
                if albums['items']:
                    df_final.at[i, 'Último Lanzamiento'] = albums['items'][0]['name']
                    df_final.at[i, 'Fecha'] = albums['items'][0]['release_date']
            except Exception as e:
                continue

# --- 4. INTERFAZ ---
st.sidebar.title("🎹 JATune Control")
menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Auditoría", "Exportar"])

if menu == "Dashboard":
    st.title("🚀 JATune Analytics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Catálogo", len(df_final))
    
    # Verificación de seguridad para los cálculos
    audiencia = df_final['Seguidores'].sum() if 'Seguidores' in df_final.columns else 0
    pop_avg = df_final['Popularidad'].mean() if 'Popularidad' in df_final.columns else 0
    
    c2.metric("Audiencia Total", f"{audiencia:,}")
    c3.metric("Pop. Promedio", f"{int(pop_avg)}%")

    st.markdown("---")
    if audiencia > 0:
        fig = px.bar(df_final, x="Artista", y="Popularidad", color="Autor", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Conexión establecida pero no se reciben datos. Verifica que tu App en Spotify esté 'Active' y tu correo en 'User Management'.")

elif menu == "Auditoría":
    st.title("🔍 Auditoría")
    for _, row in df_final.iterrows():
        with st.expander(f"📌 {row['Artista']}"):
            col1, col2 = st.columns([1, 3])
            if row['Imagen'] != "N/A" and row['Imagen']: col1.image(row['Imagen'], width=100)
            col2.write(f"**Último:** {row['Último Lanzamiento']}")
            col2.write(f"**Distribuidor:** {row['Distribuidor']}")
            col2.write(f"**Seguidores:** {row['Seguidores']:,}")

elif menu == "Exportar":
    st.title("📦 Exportar")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_final.drop(columns=['Imagen']).to_excel(writer, index=False)
    st.download_button("📥 Descargar Excel", output.getvalue(), "JATune_Report.xlsx")
