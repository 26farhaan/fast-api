from typing import Optional
from sqlmodel import SQLModel, Field


class HeroBase(SQLModel):
    name: str
    age: Optional[int] = None
    secret_name: str

# untuk input / payload


class HeroCreate(HeroBase):
    pass

# untuk model database


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
