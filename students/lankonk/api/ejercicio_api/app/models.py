from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.type = "string"
        field_schema.example = "507f1f77bcf86cd799439011"

class ItemCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""

class ItemResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombre: str
    descripcion: Optional[str] = ""

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
