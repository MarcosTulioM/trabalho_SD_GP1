import paho.mqtt.client as mqtt
import time
import json
import random
import os
from datetime import datetime

# Pega o ID do Docker Compose
CAR_ID = int(os.getenv("CAR_ID", 1)) 
BROKER = "mqtt_broker"
TOPIC = f"f1/carro{CAR_ID}/pneus"

client = mqtt.Client(f"CarroUnitario-{CAR_ID}")

# Espera o broker subir
time.sleep(5) 

try:
    conectado = False
    while not conectado:
        try:
            client.connect(BROKER, 1883, 60)
            conectado = True
        except:
            time.sleep(1)
            
    print(f"Carro {CAR_ID} conectado e pronto para a largada!")
    
    volta_atual = 0  
    
    while True:

        # Simulação das voltas de uma corrida
        if volta_atual < 16 :
            volta_atual += 1
        else:
            volta_atual = 0
        
        # Gera dados simulados
        dados = {
            "carro_id": CAR_ID,
            "pressao": round(random.uniform(20.0, 30.0), 2),
            "temperatura": round(random.uniform(80.0, 120.0), 1),
            "desgaste": round(random.uniform(0.0, 100.0), 1),
            "timestamp": datetime.now().isoformat(), # A vírgula está aqui!
            "volta": volta_atual
        }
        
        payload = json.dumps(dados)
        client.publish(TOPIC, payload)
        print(f"Carro {CAR_ID} | Volta {volta_atual} | Enviado")
        
        # Delay aleatório
        time.sleep(5 + random.uniform(0, 2)) 

except Exception as e:
    print(f"Erro no carro: {e}")