from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: Optional[int] = Field(default=None, index=True)
    secret_name: str
