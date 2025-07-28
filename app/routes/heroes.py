from typing_extensions import Annotated
from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from app.deps import SessionDep
from app.schemas.heroes import HeroCreate, Hero


router = APIRouter()


@router.post("")
def create_hero(hero: HeroCreate, session: SessionDep) -> Hero:
    db_hero = Hero(**hero.dict())
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return list(heroes)


@router.get("/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.delete("/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
