import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from typing import List
from models import ItemCreate, ItemResponse

app = FastAPI()

# Conexión a MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client.mi_base_de_datos
collection = db.items

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.get("/items", response_model=List[ItemResponse])
def get_items():
    items = []
    for item in collection.find():
        items.append(ItemResponse(
            id=str(item["_id"]),
            nombre=item["nombre"],
            descripcion=item.get("descripcion", "")
        ))
    return items

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    new_item = {
        "nombre": item.nombre,
        "descripcion": item.descripcion
    }
    result = collection.insert_one(new_item)
    return ItemResponse(
        id=str(result.inserted_id),
        nombre=new_item["nombre"],
        descripcion=new_item["descripcion"]
    )

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: str):
    try:
        obj_id = ObjectId(item_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")
        
    item = collection.find_one({"_id": obj_id})
    if item:
        return ItemResponse(
            id=str(item["_id"]),
            nombre=item["nombre"],
            descripcion=item.get("descripcion", "")
        )
    raise HTTPException(status_code=404, detail="Item no encontrado")
