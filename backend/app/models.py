from pydantic import BaseModel
from typing import Literal

class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str
    role: Literal["user", "admin"] = "user"

class UserOut(BaseModel):
    id: int
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class WorldCupItem(BaseModel):
    id: int
    name: str
    emoji: str
    category_id: int

class WorldCupCategory(BaseModel):
    id: int
    name: str
    emoji: str
    active: bool = True
    items: list[WorldCupItem] = []
