from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.deps import get_current_user_from_cookie
from models import create_db_and_tables
from .routes import auth, users, heroes  # import router
import sys

print("Python Executable:", sys.executable)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# include routers
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user_from_cookie)],
    responses={418: {"description": "I'm a teapot"}},
)
app.include_router(
    heroes.router,
    prefix="/heroes",
    tags=["Heroes"],
    dependencies=[Depends(get_current_user_from_cookie)],
    responses={418: {"description": "I'm a teapot"}},
)
