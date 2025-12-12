from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class DataSchema(BaseModel):
    data: str

    class Config:
        orm_mode = True