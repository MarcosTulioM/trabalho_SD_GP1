import paho.mqtt.client as mqtt
import grpc
import json
import os
import sys
import time


try:
    import pneus_pb2
    import pneus_pb2_grpc
except ImportError as e: # Capture o erro exato
    print(f"ERRO CRÍTICO DE IMPORTAÇÃO: {e}")
    print("Arquivos pneus_pb2.py não encontrados! Verifique o Dockerfile.")
    sys.exit(1)

# Configurações
MQTT_BROKER = "mqtt_broker"
MQTT_TOPIC = "f1/+/pneus" 
SSACP_HOST = os.getenv("SSACP_HOST", "ssacp:50051")

print(f"Iniciando ISCCP conectando ao Broker: {MQTT_BROKER} e SSACP: {SSACP_HOST}")

# Espera o SSACP subir antes de tentar conectar 
channel = grpc.insecure_channel(SSACP_HOST)
stub = pneus_pb2_grpc.PneuStorageStub(channel)

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
            timestamp=str(dados_json.get("timestamp", "")),
            volta=int(dados_json.get("volta", 0))
        )
        
        # Envia para o SSACP via gRPC
        response = stub.EnviarDadosPneu(dados_grpc)
        
        if response.sucesso:
            print(f"Salvo no Mongo! ID: {response.mensagem}")
        else:
            print(f"SSACP rejeitou: {response.mensagem}")
            
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

# Loop de conexão resiliente
while True:
    try:
        client.connect(MQTT_BROKER, 1883, 60)
        client.subscribe(MQTT_TOPIC)
        print(f"Ouvindo tópico: {MQTT_TOPIC}")
        client.loop_forever()
    except Exception as e:
        print(f"Falha na conexão MQTT ({e}). Tentando em 5s...")
        time.sleep(5)   