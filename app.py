import st
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

# --- CONFIGURACIÓN DEL BOT ---
def iniciar_bot():
    user = os.environ.get('SPOTIFY_USER')
    password = os.environ.get('SPOTIFY_PASS')
    
    if not user or not password:
        return "Error: No hay credenciales en Render."

    # Configuración de Chrome para Render (Modo Invisible)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # 1. Login
        driver.get("https://artists.spotify.com/c/dashboard")
        wait = WebDriverWait(driver, 20)
        
        # Esperar y escribir usuario
        user_input = wait.until(EC.presence_of_element_located((By.ID, "login-username")))
        user_input.send_keys(user)
        
        pass_input = driver.find_element(By.ID, "login-password")
        pass_input.send_keys(password)
        
        driver.find_element(By.ID, "login-button").click()
        
        # 2. Navegar por los 16 artistas
        # Aquí el bot buscará el selector de artista y extraerá los números
        time.sleep(10) # Esperar a que cargue el dashboard
        
        # --- LÓGICA DE EXTRACCIÓN ---
        # El bot leerá los elementos de la tabla de "Streams" y "Listeners"
        # NOTA: Los selectores de Spotify cambian, el bot buscará etiquetas 'data-testid'
        streams_xpath = "//span[contains(@class, 'TotalCount')]" 
        elementos = driver.find_elements(By.XPATH, streams_xpath)
        
        datos_reales = []
        # (Aquí el bot recorre tu lista de 16 y guarda los resultados)
        # Por ahora devolveremos un mensaje de éxito con la conexión establecida
        
        return "Sincronización Exitosa: Bot conectado a JATune"

    except Exception as e:
        return f"Error en el bot: {str(e)}"
    finally:
        driver.quit()

# --- INTERFAZ BEATJATUNE ---
st.title("🤖 BeatJATune: Bot de Sincronización")

if st.button("🚀 ACTIVAR BOT (SELENIUM)"):
    with st.spinner("El bot está entrando a Spotify for Artists..."):
        resultado = iniciar_bot()
        st.write(resultado)
