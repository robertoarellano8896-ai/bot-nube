from flask import Flask
import threading
import time
from iqoptionapi.stable_api import IQ_Option
import os

app = Flask(__name__)

# --- CONFIGURACIÓN REAL ---
EMAIL = os.getenv("robertoarellano 8896@gmail.com")
PASSWORD = os.getenv("1121Camilita")

# Si no pusiste variables en Render, ponlo aquí (RIESGO: queda público)
if not EMAIL:
    EMAIL = "TU_CORREO_AQUI@gmail.com"
if not PASSWORD:
    PASSWORD = "TU_CLAVE_AQUI"

ACTIVO = "EURUSD"
MONTO = 1  # 1 dolar por operacion - NO LO SUBAS AUN
STOP_LOSS_DIA = 10  # Si pierde 10 dolares hoy, se detiene

estado = "Iniciando en REAL..."
perdida_hoy = 0

def operar_bot():
    global estado, perdida_hoy
    try:
        estado = "Conectando a IQ Option REAL..."
        print(estado)
        API = IQ_Option(EMAIL, PASSWORD)
        check, reason = API.connect()
        
        if not check:
            estado = f"Error login REAL: {reason} - Revisa correo/clave"
            print(estado)
            return

        # --- CAMBIO A REAL ALTIRO ---
        API.change_balance("REAL")
        balance = API.get_balance()
        estado = f"¡CONECTADO EN REAL! Balance: ${balance} | {ACTIVO} | Monto: ${MONTO}"
        print(estado)

        while True:
            if perdida_hoy >= STOP_LOSS_DIA:
                estado = f"STOP LOSS ALCANZADO: Perdida hoy ${perdida_hoy}. Bot detenido por seguridad."
                print(estado)
                time.sleep(3600) # Duerme 1 hora
                continue

            # --- ESTRATEGIA SIMPLE (puedes mejorarla después) ---
            velas = API.get_candles(ACTIVO, 60, 3, time.time())
            if not velas:
                time.sleep(5)
                continue

            vela_anterior = velas[-2]
            direccion = "call" if vela_anterior['close'] > vela_anterior['open'] else "put"
            
            # Comprar
            check, id = API.buy(MONTO, ACTIVO, direccion, 1)
            
            if check:
                estado = f"[{time.strftime('%H:%M:%S')}] ORDEN REAL {direccion.upper()} en {ACTIVO} por ${MONTO} | Balance: ${API.get_balance()} | Perdida hoy: ${perdida_hoy}"
                print(estado)
                # Esperar resultado
                if API.check_win_v3(id):
                    ganancia = API.get_balance() - balance
                    if ganancia < 0:
                        perdida_hoy += abs(ganancia)
                    balance = API.get_balance()
                else:
                    perdida_hoy += MONTO
            
            time.sleep(70) # Espera a que cierre la vela + 10 seg

    except Exception as e:
        estado = f"ERROR REAL: {e}"
        print(estado)

hilo = threading.Thread(target=operar_bot)
hilo.daemon = True
hilo.start()

@app.route('/')
def home():
    return f"<h1>BOT REAL ACTIVO - {ACTIVO}</h1><p>{estado}</p><p style='color:red'>MODO REAL - Operando con dinero real</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
