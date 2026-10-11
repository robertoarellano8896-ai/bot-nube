from flask import Flask
import threading
import time
from iqoptionapi.stable_api import IQ_Option
import os

app = Flask(__name__)

EMAIL = os.getenv("IQ_EMAIL")
PASSWORD = os.getenv("IQ_PASSWORD")

ACTIVO = "EURUSD"
MONTO = 1
STOP_LOSS_DIA = 10
estado = "Iniciando en REAL..."
perdida_hoy = 0

def operar_bot():
    global estado, perdida_hoy
    try:
        estado = "Conectando a REAL..."
        API = IQ_Option(EMAIL, PASSWORD)
        check, reason = API.connect()
        if not check:
            estado = f"Error login: {reason}"
            return
        API.change_balance("REAL")
        balance = API.get_balance()
        estado = f"CONECTADO REAL! Balance ${balance}"
        while True:
            if perdida_hoy >= STOP_LOSS_DIA:
                estado = f"STOP LOSS ${perdida_hoy} - Pausado"
                time.sleep(3600)
                continue
            velas = API.get_candles(ACTIVO, 60, 3, time.time())
            if not velas:
                time.sleep(5)
                continue
            vela = velas[-2]
            direccion = "call" if vela['close'] > vela['open'] else "put"
            check, id = API.buy(MONTO, ACTIVO, direccion, 1)
            if check:
                estado = f"ORDEN REAL {direccion} ${MONTO} | Balance ${API.get_balance()}"
                time.sleep(70)
            else:
                time.sleep(10)
    except Exception as e:
        estado = f"ERROR: {e}"

threading.Thread(target=operar_bot, daemon=True).start()

@app.route('/')
def home():
    return f"<h1>BOT REAL ACTIVO</h1><p>{estado}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
