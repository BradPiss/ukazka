from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ItemCreate(BaseModel):
    nazev: str = Field(min_length=1)
    popis: Optional[str] = None
    cena: float

class Item(ItemCreate):
    id: int
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None
    
class UserPublic(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    roles: list[str] = ["user"]
    is_active: bool = True
class Config: from_attributes = True
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"