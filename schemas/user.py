from pydantic import BaseModel, constr

from enum import Enum

class UserRole(Enum):
    SELLER = "SELLER"
    BUYER = "BUYER"

class UserCreate(BaseModel):
    username: constr(min_length=1) 
    password: constr(min_length=1) 
    name: constr(min_length=1) 
    role: UserRole

class User(BaseModel):
    id: int
    username: str
    name: str
    role: UserRole
    

    class Config:
        orm_mode = True
