import paho.mqtt.client as mqtt
import json
import os

name = os.environ.get("NAME", "ISCCP")

print(f"[{name}] Iniciando assinante...", flush=True)

def on_connect(client, userdata, flags, rc):
    client.subscribe("carro/+/pneu")  # escuta todos os carros

def on_message(client, userdata, msg):
    dados = json.loads(msg.payload.decode())
    print(f"Recebido de {msg.topic}: {dados}", flush=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt_broker", 1883, 60)
client.loop_forever()
