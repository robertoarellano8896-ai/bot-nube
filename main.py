# --- CONFIGURACIÓN REAL ---
EMAIL = os.getenv("IQ_EMAIL")
PASSWORD = os.getenv("IQ_PASSWORD")

# Si no pusiste variables en Render, ponlo aquí (RIESGO: queda público)
if not EMAIL:
    EMAIL = "TU_CORREO_AQUI@gmail.com"
if not PASSWORD:
    PASSWORD = "TU_CLAVE_AQUI"
