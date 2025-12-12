import paho.mqtt.client as mqtt
import grpc
import json
import os
import sys

import pneus_pb2
import pneus_pb2_grpc

# Configurações
MQTT_BROKER = "mqtt_broker"
MQTT_TOPIC = "f1/+/pneus"
SSACP_HOST = os.getenv("SSACP_HOST", "ssacp:50051")

print(f"🔌 Iniciando ISCCP conectando ao Broker: {MQTT_BROKER} e SSACP: {SSACP_HOST}")

# Configura o canal gRPC para falar com o SSACP
channel = grpc.insecure_channel(SSACP_HOST)
stub = pneus_pb2_grpc.PneuStorageStub(channel)

# Função chamada quando chega mensagem do MQTT
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Recebido MQTT: {payload}")
        
        dados_json = json.loads(payload)
        
        # Cria o objeto gRPC
        dados_grpc = pneus_pb2.DadosPneu(
            carro_id=int(dados_json.get("carro_id", 0)),
            pressao=float(dados_json.get("pressao", 0.0)),
            temperatura=float(dados_json.get("temperatura", 0.0)),
            desgaste=float(dados_json.get("desgaste", 0.0)),
            timestamp=str(dados_json.get("timestamp", ""))
        )
        
        # Envia para o SSACP via gRPC
        response = stub.EnviarDadosPneu(dados_grpc)
        
        if response.sucesso:
            print(f"Salvo no Mongo pelo SSACP! (Msg: {response.mensagem})")
        else:
            print(f"SSACP rejeitou: {response.mensagem}")
            
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# Configura o MQTT
client = mqtt.Client()
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.subscribe(MQTT_TOPIC)
    print(f"Ouvindo tópico: {MQTT_TOPIC}")
    client.loop_forever()
except Exception as e:
    print(f"Erro fatal no MQTT: {e}")