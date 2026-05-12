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
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { border: 1px solid #30363d; padding: 15px; border-radius: 10px; background-color: #161b22; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; background-color: #0d1117; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. AUTENTICACIÓN CORREGIDA ---
try:
    # Aquí llamamos al NOMBRE que pusiste en el cuadro de texto de Streamlit
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    st.error("🔑 Error: No se encontraron los nombres 'SPOTIPY_CLIENT_ID' y 'SPOTIPY_CLIENT_SECRET' en los Secrets.")
    st.info("Asegúrate de que en el cuadro de texto de Streamlit pegaste los nombres tal cual, así:")
    st.code('SPOTIPY_CLIENT_ID = "d9a0a75ae8644699884d71c15c58e563"\nSPOTIPY_CLIENT_SECRET = "a45b08ed2d544142a6b7b18a48e06b08"')
    st.stop()

# --- 2. BASE DE DATOS JATUNE ---
data_label = {
    "Artista": ["Jeantune", "JCSTUDIO", "JMAR", "YlegMoon", "Batytune", "Jzentrix", "JironPulse", "God Herd", "JJ Legacy", "Cielaurum", "QuietMetric", "AetherFocus", "ZukiPop", "LexiGo", "VYRONEX", "AEROVIA"],
    "Autor": ["Jean C", "Jean C", "Jean C", "Angely", "Angely", "Dari", "Micha", "Jean C", "Jean C", "Angely", "Dari", "Jean C", "Jean C", "Jean C", "Jean C", "Jean C"],
    "Distribuidor": ["Distrokid", "Distrokid", "Ditto", "Distrokid", "Distrokid", "Distrokid", "Distrokid", "TuneCore", "Symphonic", "Ditto", "Ditto", "Ditto", "Distrokid", "Distrokid", "Distrokid", "Distrokid"]
}
df_label = pd.DataFrame(data_label)

# --- 3. FUNCIONES DE EXTRACCIÓN ---
@st.cache_data(ttl=3600)
def get_full_artist_data(nombre):
    try:
        search = sp.search(q=f'artist:{nombre}', type='artist', limit=1)
        if not search['artists']['items']: return None
        a = search['artists']['items'][0]
        
        # Obtener último lanzamiento
        albums = sp.artist_albums(a['id'], album_type='single,album', limit=1)
        last_release = albums['items'][0]['name'] if albums['items'] else "N/A"
        release_date = albums['items'][0]['release_date'] if albums['items'] else "N/A"
        
        return {
            "Spotify_ID": a['id'],
            "Seguidores": a['followers']['total'],
            "Popularidad": a['popularity'],
            "Último Lanzamiento": last_release,
            "Fecha": release_date,
            "Imagen": a['images'][0]['url'] if a['images'] else None
        }
    except:
        return None

# --- 4. PROCESAMIENTO (CORREGIDO) ---
with st.spinner('Sincronizando con Spotify API...'):
    # Obtenemos los datos de cada artista
    results = []
    for name in df_label["Artista"]:
        data = get_full_artist_data(name)
        if data:
            # Añadimos el nombre para tener una columna en común para el "merge"
            data["Artista"] = name
            results.append(data)
    
    # Creamos el DataFrame de métricas
    df_metrics = pd.DataFrame(results)
    
    if not df_metrics.empty:
        # Unimos los datos del sello con los de Spotify usando la columna "Artista"
        df_final = pd.merge(df_label, df_metrics, on="Artista", how="left")
    else:
        # Si falla la API, mantenemos los datos básicos para que no crashee
        df_final = df_label.copy()
        for col in ["Seguidores", "Popularidad", "Último Lanzamiento", "Fecha"]:
            df_final[col] = 0 if col in ["Seguidores", "Popularidad"] else "N/A"

# Limpieza: eliminar duplicados si existen por errores de re-ejecución
df_final = df_final.loc[:,~df_final.columns.duplicated()]

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
    st.write("Verifica que tus distribuidoras hayan indexado correctamente los últimos tracks.")
    
    for _, row in df_final.iterrows():
        with st.expander(f"📌 {row['Artista']} ({row['Distribuidor']})"):
            c1, c2 = st.columns([1, 3])
            if row['Imagen']: c1.image(row['Imagen'], width=100)
            c2.write(f"**Último lanzamiento:** {row['Último Lanzamiento']}")
            c2.write(f"**Fecha:** {row['Fecha']}")
            c2.write(f"**Spotify ID:** `{row['Spotify_ID']}`")

# --- MÓDULO: EXPORTAR ---
elif menu == "Exportar Reportes":
    st.title("📦 Gestión de Archivos")
    st.write("Descarga la data actual en formato Excel para reportes administrativos.")
    
    # Generar Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_final.drop(columns=['Imagen']).to_excel(writer, index=False, sheet_name='Data_JATune')
    
    st.download_button(
        label="📥 Descargar Reporte Excel",
        data=output.getvalue(),
        file_name="Reporte_JATune_Spotify.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
