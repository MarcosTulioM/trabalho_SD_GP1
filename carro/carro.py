import paho.mqtt.client as mqtt
import time
import random
import json
import os

client = mqtt.Client()
client.connect("mqtt_broker", 1883, 60)  #Container do Mosquitto no docker

carro_id = os.environ.get("CAR_ID", "0")
print(f"[carro {carro_id}] Iniciando publicador...", flush=True)

def gerar_dados_pneu():
    return {
        "pressao": round(random.uniform(18.0, 22.0), 2),
        "temperatura": round(random.uniform(70.0, 100.0), 2)
    }

while True:
    dados = gerar_dados_pneu()
    topico = f"carro/{carro_id}/pneu"
    client.publish(topico, json.dumps(dados))
    print(f"[carro {carro_id}] Publicado: {topico} -> {dados}", flush=True)
    time.sleep(5)
