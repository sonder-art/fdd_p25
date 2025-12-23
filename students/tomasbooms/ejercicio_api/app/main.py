from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from datetime import datetime

app = FastAPI(title="FastAPI con MongoDB", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://admin:password123@mongodb:27017/mydb?authSource=admin")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.mydb
collection = db.items


# Pydantic models
class Item(BaseModel):
    name: str = Field(..., description="Nombre del item")
    description: Optional[str] = Field(None, description="Descripción del item")
    price: float = Field(..., gt=0, description="Precio del item")
    created_at: Optional[datetime] = None


class ItemResponse(Item):
    id: str

    class Config:
        from_attributes = True


# Database connection check
@app.on_event("startup")
async def startup_db_client():
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ Conectado a MongoDB exitosamente")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


# Routes
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a FastAPI con MongoDB",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    try:
        await client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: Item):
    item_dict = item.model_dump()
    item_dict["created_at"] = datetime.utcnow()
    
    result = await collection.insert_one(item_dict)
    created_item = await collection.find_one({"_id": result.inserted_id})
    created_item["id"] = str(created_item["_id"])
    del created_item["_id"]
    
    return ItemResponse(**created_item)


@app.get("/items", response_model=List[ItemResponse])
async def get_items(skip: int = 0, limit: int = 10):
    cursor = collection.find().skip(skip).limit(limit)
    items = []
    async for item in cursor:
        item["id"] = str(item["_id"])
        del item["_id"]
        items.append(ItemResponse(**item))
    return items


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    from bson import ObjectId
    try:
        item = await collection.find_one({"_id": ObjectId(item_id)})
        if item is None:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        item["id"] = str(item["_id"])
        del item["_id"]
        return ItemResponse(**item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID inválido: {str(e)}")


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: str):
    from bson import ObjectId
    try:
        result = await collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID inválido: {str(e)}")




