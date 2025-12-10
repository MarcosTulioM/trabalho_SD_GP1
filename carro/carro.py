import paho.mqtt.client as mqtt
import time
import json
import random
import os
from datetime import datetime

CAR_ID = int(os.getenv("CAR_ID", 1))
BROKER = "mqtt_broker"
TOPIC = f"f1/carro{CAR_ID}/pneus"

client = mqtt.Client()

# Espera o broker subir
time.sleep(5) 

try:
    client.connect(BROKER, 1883, 60)
    print(f"🏎️ Carro {CAR_ID} conectado! Enviando dados...")
    
    while True:
        # Gera dados simulados
        dados = {
            "carro_id": CAR_ID,
            "pressao": round(random.uniform(20.0, 30.0), 2),
            "temperatura": round(random.uniform(80.0, 120.0), 1),
            "desgaste": round(random.uniform(0.0, 100.0), 1),
            "timestamp": datetime.now().isoformat()
        }
        
        payload = json.dumps(dados)
        client.publish(TOPIC, payload)
        print(f"📤 Enviado: {payload}")
        
        time.sleep(5) # Envia a cada 5 segundos

except Exception as e:
    print(f"Erro no carro: {e}")