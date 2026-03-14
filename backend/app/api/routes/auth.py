import uuid as uuid_module
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.api.schemas.auth import UserCreate, UserLogin, AuthResponse, UserResponse
from app.services.auth_service import AuthService
from app.database.session import get_db
from app.models.user import User
from app.config import settings

router = APIRouter()


def _build_auth_response(user: User) -> dict:
    return {
        "access_token": AuthService.create_token(str(user.id)),
        "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRATION_HOURS * 3600,
        "user": user,
    }


@router.post("/register", response_model=AuthResponse)
async def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = AuthService.create_user(db, data.email, data.password, data.full_name)
    return _build_auth_response(user)


@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return _build_auth_response(user)


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    """Dependency: validates Bearer token and returns the User ORM object."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header")

    token = authorization.split(" ", 1)[1]
    user_id_str = AuthService.decode_token(token)
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    try:
        uid = uuid_module.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
