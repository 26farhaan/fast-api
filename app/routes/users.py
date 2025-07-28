from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from fastapi import Body, Path
from sqlmodel import select

from app.schemas.users import UserCreate, UserRead
from app.models.users import User
from app.core.security import hash_password
from app.deps import SessionDep


router = APIRouter(tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(
    user_in: Annotated[UserCreate, Body()],
    session: SessionDep
):
    user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        birthday=user_in.birthday,
        address=user_in.address,
        hashed_password=hash_password(user_in.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=list[UserRead])
def get_users(session: SessionDep):
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: Annotated[int, Path()],
    session: SessionDep
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: Annotated[int, Path()],
    update_data: Annotated[dict, Body()],
    session: SessionDep
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in update_data.items():
        if key == "password":
            value = hash_password(value)
            key = "hashed_password"
        if hasattr(user, key):
            setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: Annotated[int, Path()],
    session: SessionDep
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"deleted": True}
