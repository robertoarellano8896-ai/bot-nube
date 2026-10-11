from flask import Flask
import threading
import time
from iqoptionapi.stable_api import IQ_Option
import os

app = Flask(__name__)

# --- CONFIGURACIÓN - CAMBIA ESTO ---
# Pon tu correo y clave de IQ Option en Render > Environment (más seguro)
# Por ahora las dejamos aquí para que funcione rápido

EMAIL = os.getenv("IQ_EMAIL", "robertoarellano8896@gmail.com")
PASSWORD = os.getenv("IQ_PASSWORD", "1121Camilita")
MONTO = 1 # 1 dolar por operacion
ACTIVO = "EURUSD" # Par que va a operar
TIEMPO_EXPIRACION = 1 # 1 minuto

bot_activo = False
estado = "Esperando iniciar..."

def operar_bot():
    global bot_activo, estado
    try:
        estado = "Conectando a IQ Option..."
        print(estado)
        I_want_money = IQ_Option(EMAIL, PASSWORD)
        check, reason = I_want_money.connect()

        if not check:
            estado = f"Error de conexion: {reason}"
            print(estado)
            return

        # Cambiar a cuenta PRACTICA para no perder plata real al inicio
        I_want_money.change_balance("PRACTICE")
        balance = I_want_money.get_balance()
        estado = f"Conectado! Balance Practica: ${balance} | Activo: {ACTIVO}"
        print(estado)
        bot_activo = True

        while bot_activo:
            # --- AQUI VA TU ESTRATEGIA SIMPLE ---
            # Ejemplo: Estrategia de velas - muy básica para probar

            # Obtenemos velas de 1 minuto
            velas = I_want_money.get_candles(ACTIVO, 60, 3, time.time())

            if len(velas) >= 3:
                vela_anterior = velas[1] # la penultima cerrada
                # Si la vela anterior fue VERDE (subio), compramos CALL
                if vela_anterior['close'] > vela_anterior['open']:
                    I_want_money.buy(MONTO, ACTIVO, "call", TIEMPO_EXPIRACION)
                    estado = f"[{time.strftime('%H:%M:%S')}] COMPRA CALL en {ACTIVO} - Balance: {I_want_money.get_balance()}"
                    print(estado)
                else: # Si fue ROJA, compramos PUT
                    I_want_money.buy(MONTO, ACTIVO, "put", TIEMPO_EXPIRACION)
                    estado = f"[{time.strftime('%H:%M:%S')}] COMPRA PUT en {ACTIVO} - Balance: {I_want_money.get_balance()}"
                    print(estado)

            time.sleep(60) # Espera 1 minuto entre operaciones

    except Exception as e:
        estado = f"Error bot detenido: {e}"
        print(estado)
        bot_activo = False

# Iniciar el bot en segundo plano
hilo = threading.Thread(target=operar_bot)
hilo.daemon = True
hilo.start()

@app.route('/')
def home():
    global estado
    return f"""
    <h1>Bot IQ Option 24/7 - LISTO</h1>
    <p><b>Estado:</b> {estado}</p>
    <p><b>Activo:</b> {ACTIVO}</p>
    <p><b>Link:</b> bot-nube.onrender.com</p>
    <p>Si ves esto, el bot esta en la nube trabajando.</p>
    <hr>
    <p><small>Modo PRACTICA activado. Cambia a REAL solo cuando estes seguro.</small></p>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
