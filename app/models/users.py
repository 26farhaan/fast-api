from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    birthday: date
    address: Optional[str] = None
    role: str = Field(default="user")  # user / admin
    hashed_password: str
