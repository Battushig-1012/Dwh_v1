from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth.deps import get_current_user
from ..auth.security import authenticate_user, create_access_token
from ..config import settings
from ..db import get_db

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str
    demo_mode: bool = False


@router.post("/auth/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session | None = Depends(get_db)):
    user = authenticate_user(db, body.username, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user["username"], user["role_code"], user["full_name"])
    return TokenResponse(
        access_token=token,
        role=user["role_code"],
        full_name=user["full_name"],
        demo_mode=settings.demo_mode,
    )


@router.get("/auth/me")
def me(user: dict = Depends(get_current_user)):
    return {**user, "demo_mode": settings.demo_mode}
