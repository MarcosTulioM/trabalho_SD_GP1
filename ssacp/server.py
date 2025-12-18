from concurrent import futures
import grpc
import pymongo
import os
import time
import sys

import pneus_pb2
import pneus_pb2_grpc

MONGO_URI = os.getenv("MONGO_URL", "mongodb://root:example@mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0&authSource=admin")

class PneuStorageService(pneus_pb2_grpc.PneuStorageServicer):
    def __init__(self):
        self.db = None
        self.collection = None
        self._conectar_mongo()

    def _conectar_mongo(self):
        while True:
            try:
                print(f"Tentando conectar ao MongoDB em: {MONGO_URI} ...")
                client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
                client.server_info() 
                self.db = client["f1_telemetry"]
                self.collection = self.db["pneus"]
                print(f"SUCESSO! Conectado ao MongoDB: {client.server_info()['version']}")
                break
            except Exception as e:
                print(f"Falha na conexão ({e}). Tentando novamente em 5s...")
                time.sleep(5)

    def EnviarDadosPneu(self, request, context):
        print(f"Recebido dados do Carro {request.carro_id}")
        documento = {
            "carro_id": request.carro_id,
            "pressao": request.pressao,
            "temperatura": request.temperatura,
            "desgaste": request.desgaste,
            "timestamp": request.timestamp,
            "volta": request.volta
        }
        try:
            result = self.collection.insert_one(documento)
            return pneus_pb2.RespostaArmazenamento(sucesso=True, mensagem=f"Salvo ID: {result.inserted_id}")
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return pneus_pb2.RespostaArmazenamento(sucesso=False, mensagem=str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    pneus_pb2_grpc.add_PneuStorageServicer_to_server(PneuStorageService(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor SSACP gRPC rodando na porta 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()