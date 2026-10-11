from flask import Flask
import threading
import time
from iqoptionapi.stable_api import IQ_Option
import os

app = Flask(__name__)

EMAIL = os.getenv("IQ_EMAIL", "robertoarellano8896@gmail.com")
PASSWORD = os.getenv("IQ_PASSWORD", "1121Camilita")
ACTIVO = "EURUSD"
MONTO = 1

bot_activo = False
estado = "Bot iniciado"

def operar_bot():
    global estado
    print("Bot en la nube funcionando")

hilo = threading.Thread(target=operar_bot)
hilo.daemon = True
hilo.start()

@app.route('/')
def home():
    return f"<h1>BOT NUBE LIVE 24/7</h1><p>{estado}</p><p>Activo: {ACTIVO}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
