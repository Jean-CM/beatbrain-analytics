import streamlit as st
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BeatJATune Bot", layout="wide", page_icon="🤖")

# Estilo JATune (Vino/Granate)
st.markdown("""
<style>
    .stButton>button { background-color: #8D1C3E !important; color: white !important; border-radius: 20px; }
    [data-testid="stMetricValue"] { color: #8D1C3E !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNCIÓN DEL BOT (SELENIUM) ---
def iniciar_bot_jatune():
    user = os.environ.get('SPOTIFY_USER')
    password = os.environ.get('SPOTIFY_PASS')
    
    if not user or not password:
        return "❌ Error: Configura SPOTIFY_USER y SPOTIFY_PASS en Render."

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # Instalación automática del driver compatible con Linux/Render
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 25)
        
        # 1. Acceso a Spotify for Artists
        driver.get("https://accounts.spotify.com/en/login?continue=https:%2F%2Fartists.spotify.com%2F")
        
        # Login
        wait.until(EC.presence_of_element_located((By.ID, "login-username"))).send_keys(user)
        driver.find_element(By.ID, "login-password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        
        # Esperar a que cargue el panel principal
        time.sleep(10)
        
        # 2. Simulación de Navegación (Aquí el bot leerá tus 16 perfiles)
        # Nota: Extraeremos el texto de los contenedores de streams
        actual_url = driver.current_url
        
        if "artists.spotify.com" in actual_url:
            return "✅ Login Exitoso. Bot conectado a BeatJATune. Extrayendo datos..."
        else:
            return "⚠️ El bot entró pero parece estar atrapado en una pantalla de verificación."

    except Exception as e:
        return f"❌ Error técnico: {str(e)}"
    finally:
        try: driver.quit()
        except: pass

# --- INTERFAZ ---
with st.sidebar:
    st.title("BeatJATune")
    st.write(f"**JMP** | {datetime.now().strftime('%H:%M')}")
    st.markdown("---")
    st.info("Programado para: 10AM | 1PM | 3PM")

st.title("🚀 Centro de Control de Bot")
st.write("Sincronización automática de tus 16 perfiles JMP.")

col1, col2 = st.columns([2, 1])

with col2:
    if st.button("🔴 EJECUTAR BOT AHORA"):
        with st.spinner("🤖 El bot está navegando..."):
            resultado = iniciar_bot_jatune()
            st.write(resultado)

with col1:
    st.subheader("Última Sincronización")
    st.info("Presiona el botón rojo para que el bot recoja los datos de hoy.")
