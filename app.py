import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
from io import BytesIO

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JATune Command Center v2", layout="wide", page_icon="🚀")

# Estilo Ejecutivo (Dark Mode & Accents)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9
    d1d9; }
    .stMetric { border: 1px solid #30363d; padding: 15px; border-radius: 10px; background-color: #161b22; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; background-color: #0d1117; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. AUTENTICACIÓN ---
if "SPOTIPY_CLIENT_ID" not in st.secrets or "SPOTIPY_CLIENT_SECRET" not in st.secrets:
    st.error("❌ Los Secrets no están configurados correctamente en Streamlit Cloud.")
    st.stop()

try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    # Línea de prueba temporal
st.write(f"Conexión exitosa con ID: {sp.me()['id']}") if st.sidebar.button("Probar Conexión") else None
except Exception as e:
    st.error(f"⚠️ Error de conexión con Spotify API: {e}")
    st.stop()

# --- 2. BASE DE DATOS JATUNE (BASADA EN TUS LINKS) ---
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
    "Autor": [
        "Jean C", "Jean C", "Jean C", "Angely", "Angely", 
        "Dari", "Micha", "Jean C", "Jean C", "Angely", 
        "Dari", "Jean C", "Jean C", "Jean C", "Jean C", 
        "Jean C", "Micha", "Angy"
    ],
    "Distribuidor": [
        "Distrokid", "Distrokid", "Ditto", "Distrokid", "Distrokid", 
        "Distrokid", "Distrokid", "TuneCore", "Symphonic", "Ditto", 
        "Ditto", "Ditto", "Distrokid", "Distrokid", "Distrokid", 
        "Distrokid", "Distrokid", "Symphonic"
    ]
}
df_label = pd.DataFrame(data_label)

# --- 3. FUNCIONES DE EXTRACCIÓN ---
@st.cache_data(ttl=3600)
def get_full_artist_data(artist_id):
    try:
        a = sp.artist(artist_id)
        # Obtener último lanzamiento
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
    except Exception:
        return None

# --- 4. PROCESAMIENTO ---
with st.spinner('Actualizando métricas de JATune...'):
    results = []
    for sid in df_label["Spotify_ID"]:
        res = get_full_artist_data(sid)
        if res:
            results.append(res)
        else:
            # Datos de respaldo si falla la API para un ID específico
            results.append({
                "Spotify_ID": sid,
                "Seguidores": 0,
                "Popularidad": 0,
                "Último Lanzamiento": "N/A",
                "Fecha": "N/A",
                "Imagen": None
            })
    
    df_metrics = pd.DataFrame(results)
    df_final = pd.merge(df_label, df_metrics, on="Spotify_ID", how="left")

# --- 5. INTERFAZ (SIDEBAR) ---
st.sidebar.title("🎹 JATune Control")
menu = st.sidebar.selectbox("Seleccionar Módulo", ["Dashboard Ejecutivo", "Auditoría de Lanzamientos", "Exportar Reportes"])

# --- MÓDULO: DASHBOARD ---
if menu == "Dashboard Ejecutivo":
    st.title("🚀 JATune Executive Analytics")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Catálogo Activo", len(df_final))
    m2.metric("Audiencia Total", f"{df_final['Seguidores'].sum():,}")
    m3.metric("Popularidad Promedio", f"{int(df_final['Popularidad'].mean())}%")

    st.markdown("---")
    fig = px.bar(df_final, x="Artista", y="Popularidad", color="Autor", 
                 title="Ranking de Popularidad por Identidad", template="plotly_dark",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

# --- MÓDULO: AUDITORÍA ---
elif menu == "Auditoría de Lanzamientos":
    st.title("🔍 Auditoría de Catálogo & Distribución")
    
    for _, row in df_final.iterrows():
        label_text = f"📌 {row['Artista']} ({row['Distribuidor']})"
        with st.expander(label_text):
            c1, c2 = st.columns([1, 3])
            
            if "Imagen" in row and pd.notnull(row['Imagen']):
                c1.image(row['Imagen'], width=100)
            else:
                c1.info("Sin imagen")
                
            c2.write(f"**Último lanzamiento:** {row.get('Último Lanzamiento', 'N/A')}")
            c2.write(f"**Fecha:** {row.get('Fecha', 'N/A')}")
            c2.write(f"**Spotify ID:** `{row.get('Spotify_ID', 'N/A')}`")

# --- MÓDULO: EXPORTAR ---
elif menu == "Exportar Reportes":
    st.title("📦 Gestión de Archivos")
    st.write("Descarga la data actual en formato Excel para reportes administrativos.")
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Eliminamos la columna de imagen para el Excel
        df_export = df_final.copy()
        if 'Imagen' in df_export.columns:
            df_export = df_export.drop(columns=['Imagen'])
        df_export.to_excel(writer, index=False, sheet_name='Data_JATune')
    
    st.download_button(
        label="📥 Descargar Reporte Excel",
        data=output.getvalue(),
        file_name="Reporte_JATune_Spotify.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
