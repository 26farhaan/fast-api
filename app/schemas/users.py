from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class UserCreate(BaseModel):
    email: str = Field(..., examples=["user@email.com"])
    first_name: str
    last_name: str
    birthday: date
    address: Optional[str] = None
    password: str = Field(..., min_length=6)


class UserRead(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    birthday: date
    address: Optional[str]
    role: str

    class Config:
        orm_mode = True
