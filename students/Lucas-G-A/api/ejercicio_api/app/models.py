from pydantic import BaseModel

# Modelo para CREAR un item (lo que recibes del cliente)
class ItemCreate(BaseModel):
    nombre: str
    descripcion: str = ""

# Modelo para RESPONDER (lo que devuelves al cliente)
class ItemResponse(BaseModel):
    id: str
    nombre: str
    descripcion: str
    
    class Config:
        from_attributes = True