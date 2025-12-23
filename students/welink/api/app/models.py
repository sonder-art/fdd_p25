from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""

class ItemResponse(BaseModel):
    id: str
    nombre: str
    descripcion: str
