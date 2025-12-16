from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from models import ItemCreate, ItemResponse
import os

app = FastAPI(title="API de Items", version="1.0.0")

# Conexión a MongoDB
# IMPORTANTE: Usa "db" como hostname (nombre del servicio en docker-compose)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://db:27017")
client = MongoClient(MONGO_URL)
db = client.items_db
collection = db.items

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/items", response_model=list[ItemResponse])
def listar_items():
    """Listar todos los items"""
    items = []
    for item in collection.find():
        items.append(ItemResponse(
            id=str(item["_id"]),
            nombre=item["nombre"],
            descripcion=item.get("descripcion", "")
        ))
    return items

@app.post("/items", response_model=ItemResponse, status_code=201)
def crear_item(item: ItemCreate):
    """Crear un nuevo item"""
    item_dict = item.model_dump()
    result = collection.insert_one(item_dict)
    
    # Obtener el item creado
    created_item = collection.find_one({"_id": result.inserted_id})
    return ItemResponse(
        id=str(created_item["_id"]),
        nombre=created_item["nombre"],
        descripcion=created_item.get("descripcion", "")
    )

@app.get("/items/{item_id}", response_model=ItemResponse)
def obtener_item(item_id: str):
    """Obtener un item por ID"""
    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item is None:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        
        return ItemResponse(
            id=str(item["_id"]),
            nombre=item["nombre"],
            descripcion=item.get("descripcion", "")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="ID inválido")