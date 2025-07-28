from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Response
from jose import jwt
from app.schemas.auth import LoginRequest, Token
from app.deps import (
    ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user,
    fake_users_db
)

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: LoginRequest, response: Response):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expiry_minutes = 10080 if form_data.remember_me else ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=expiry_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=expiry_minutes * 60,
        samesite="none",
        secure=True,
        path="/"
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Logged out"}
