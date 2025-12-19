from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão com o Banco 
MONGO_URI = os.getenv("MONGO_URL", "mongodb://root:example@mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0&authSource=admin")
client = MongoClient(MONGO_URI)
db = client["f1_telemetry"]
collection = db["pneus"]

@app.get("/")
def read_root():
    return {"status": "SSVCP Online", "message": "API de Telemetria F1"}

@app.get("/pneus")
def listar_pneus():
    # Retorna os últimos 20 registros, ordenados do mais recente para o mais antigo
    dados = list(collection.find({}, {"_id": 0}).sort("_id", -1).limit(20))
    return dados

@app.get("/pneus/{carro_id}")
def listar_por_carro(carro_id: int):
    # Filtra por carro específico
    dados = list(collection.find({"carro_id": carro_id}, {"_id": 0}).sort("_id", -1).limit(10))
    return dados