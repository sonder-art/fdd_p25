from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from models import ItemCreate, ItemResponse
import os

app = FastAPI(title="Items API", version="1.0.0")

# Conexión a MongoDB
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://db:27017")

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client.items_db
    collection = db.items
    # Verificar conexión
    client.server_info()
except ConnectionFailure:
    print("Error: No se pudo conectar a MongoDB")


@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/items", response_model=list[ItemResponse])
async def list_items():
    """Listar todos los items"""
    try:
        items = list(collection.find())
        return [
            ItemResponse(
                id=str(item["_id"]),
                nombre=item["nombre"],
                descripcion=item.get("descripcion", "")
            )
            for item in items
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar items: {str(e)}")


@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """Crear un nuevo item"""
    try:
        item_dict = {
            "nombre": item.nombre,
            "descripcion": item.descripcion
        }
        result = collection.insert_one(item_dict)
        created_item = collection.find_one({"_id": result.inserted_id})
        return ItemResponse(
            id=str(created_item["_id"]),
            nombre=created_item["nombre"],
            descripcion=created_item.get("descripcion", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear item: {str(e)}")


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """Obtener un item por ID"""
    try:
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item is None:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        
        return ItemResponse(
            id=str(item["_id"]),
            nombre=item["nombre"],
            descripcion=item.get("descripcion", "")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener item: {str(e)}")

