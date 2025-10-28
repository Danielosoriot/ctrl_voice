import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

# --- MQTT Configuración ---
def on_publish(client, userdata, result):
    print("El dato ha sido publicado 🔥\n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("GIT-HUBC")
client1.on_message = on_message

# --- Estilo visual inspirado en Anuel AA ---
st.markdown("""
    <style>
        /* Fondo degradado negro a rojo */
        .stApp {
            background: linear-gradient(135deg, #000000, #420000, #8B0000);
            color: white;
            font-family: 'Poppins', sans-serif;
        }

        /* Título principal */
        h1 {
            color: #ff3b3b;
            text-align: center;
            font-weight: 800;
            font-size: 2.8em;
            text-shadow: 0px 0px 20px #ff0000;
            letter-spacing: 2px;
        }

        /* Subtítulo */
        h2 {
            color: #f2b6b6;
            text-align: center;
            font-weight: 600;
            text-shadow: 0px 0px 10px #a00000;
        }

        /* Texto general */
        p, div, span {
            color: #f8f8f8 !important;
            font-size: 1.1em;
        }

        /* Imagen centrada */
        img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 20px;
            border: 3px solid #ff0000;
            box-shadow: 0px 0px 25px rgba(255, 0, 0, 0.7);
        }

        /* Botón personalizado */
        div[data-testid="stButton"] > button {
            background: linear-gradient(90deg, #ff0000, #770000);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.7em 2em;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 0px 0px 20px #ff1a1a;
            transition: all 0.3s ease;
        }

        div[data-testid="stButton"] > button:hover {
            transform: scale(1.08);
            box-shadow: 0px 0px 30px #ff3333;
        }

        /* Texto final */
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 1.2em;
            color: #ff4d4d;
            text-shadow: 0px 0px 10px #ff0000;
        }
    </style>
""", unsafe_allow_html=True)

# --- Interfaz ---
st.title("🎤 INTERFACES MULTIMODALES")
st.subheader("🔥 CONTROL POR VOZ - ESTILO ANUEL 🔥")

# Imagen
image = Image.open('voice_ctrl.jpg')
st.image(image, width=250)

st.write("Toca el botón y **habla con flow** 🎙️ — deja que tu voz mande en la acción.")

# Botón de reconocimiento de voz
stt_button = Button(label="🎧 INICIAR VOZ", width=200)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

# Escucha del evento de voz
result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# Procesamiento de voz
if result:
    if "GET_TEXT" in result:
        st.success(f"🎙️ Comando detectado: {result.get('GET_TEXT')}")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": result.get("GET_TEXT").strip()})
        ret = client1.publish("voice_ctrl", message)

        # Crea carpeta temporal si no existe
        try:
            os.mkdir("temp")
        except:
            pass

# Footer con frase icónica
st.markdown("""
<div class="footer">
    💯 Proyecto inspirado en la vibra de ANUEL AA 💯<br>
    “REAL HASTA LA MUERTE 🔥”
</div>
""", unsafe_allow_html=True)
