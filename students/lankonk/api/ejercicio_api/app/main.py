from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import os

from .models import ItemCreate, ItemResponse, PyObjectId

app = FastAPI()

mongodb_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
db_name = "mydatabase"
collection_name = "items"

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(mongodb_url)
    app.mongodb = app.mongodb_client[db_name]
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print("Disconnected from MongoDB")

@app.get("/", response_model=dict)
async def health_check():
    return {"status": "ok"}

@app.get("/items", response_model=List[ItemResponse])
async def list_items():
    items = []
    for item in await app.mongodb[collection_name].find().to_list(1000):
        items.append(ItemResponse(**item))
    return items

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    item_dict = item.dict()
    new_item = await app.mongodb[collection_name].insert_one(item_dict)
    created_item = await app.mongodb[collection_name].find_one({"_id": new_item.inserted_id})
    return ItemResponse(**created_item)

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: PyObjectId):
    if (item := await app.mongodb[collection_name].find_one({"_id": item_id})) is not None:
        return ItemResponse(**item)
    raise HTTPException(status_code=404, detail="Item not found")
