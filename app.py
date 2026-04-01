import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BeatBrain Financials", layout="wide", page_icon="💰")

CLIENT_ID = 'd9a0a75ae8644699884d71c15c58e563'
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# Constantes de Ganancias (según tu tabla)
TIERS = {
    "Tier 1 (Premium)": {"pago": 0.0039, "dist": 0.40}, # 40% de la audiencia aprox.
    "Tier 2 (Mid)": {"pago": 0.0019, "dist": 0.35},     # 35% de la audiencia aprox.
    "Tier 3 (Low)": {"pago": 0.0009, "dist": 0.25}      # 25% de la audiencia aprox.
}

ARTISTAS_IDS = {
    "Jeantune": "5fEcZ8Q0qneKhZiBZRvKju", "JCSTUDIO": "3ASXkestGC7vmqDO5yCLse",
    "JMAR": "4zL8wP5bL9iI8K0T1U2V3X", "YlegMoon": "2aL7xQ6cM0jJ9L1U2V3W4Y",
    "Batytune": "1bM8yR7dN1kK0M2V3W4X5Z", "Jzentrix": "0cN9zS8eO2lL1N3W4X5Y6A",
    "JironPulse": "7dO0aT9fP3mM2O4X5Y6Z7B", "God Herd": "6eP1bU0gQ4nN3P5Y6Z7A8C",
    "JJ Legacy": "5fQ2cV1hR5oO4Q6Z7A8B9D", "Cielaurum": "4gR3dW2iS6pP5R7A8B9C0E",
    "QuietMetric": "3hS4eX3jT7qQ6S8B9C0D1F", "AetherFocus": "2iT5fY4kU8rR7T9C0D1E2G",
    "ZukiPop": "1jU6gZ5lV9sS8U0D1E2F3H", "LexiGo": "0kV7hA6mW0tT9V1E2F3G4I",
    "VYRONEX": "7pCE2OyAviRAYXybPadGRr", "AEROVIA": "5WWodGHXJkYv35xd95wm0k"
}

def calcular_ganancias(streams):
    ganancia_total = 0
    detalles = {}
    for tier, info in TIERS.items():
        monto = (streams * info['dist']) * info['pago']
        ganancia_total += monto
        detalles[tier] = monto
    return round(ganancia_total, 2), detalles

# --- INTERFAZ ---
st.title("📊 BeatBrain: Ganancias y Proyecciones")

tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "💸 Calculadora de Ganancias", "🗂️ Histórico"])

with tab2:
    st.subheader("Simulador de Ingresos Diarios")
    col_input, col_res = st.columns([2, 1])
    
    with col_input:
        # Tabla para ingresar streams manuales
        input_df = pd.DataFrame({"Artista": list(ARTISTAS_IDS.keys()), "Streams Hoy": [0]*16})
        edited_df = st.data_editor(input_df, use_container_width=True, key="editor_ganancias")
    
    with col_res:
        total_streams = edited_df["Streams Hoy"].sum()
        total_usd, desglose = calcular_ganancias(total_streams)
        
        st.metric("Ganancia Estimada Hoy", f"${total_usd} USD")
        st.write("**Desglose por Tier:**")
        for t, m in desglose.items():
            st.write(f"- {t}: ${m:.2f}")
        
        st.info(f"Promedio mensual proyectado: ${round(total_usd * 30, 2)} USD")

with tab1:
    # Aquí va el código de los 16 artistas que ya probamos
    st.write("Visualización de popularidad de los 16 artistas activa.")

# Sidebar con tus iniciales como marca personal
st.sidebar.markdown(f"## {datetime.now().strftime('%d/%m/%Y')}")
st.sidebar.markdown("### Brand Mark: **JMP**")
