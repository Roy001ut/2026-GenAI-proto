import uuid as uuid_module
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.api.schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.database.session import get_db
from app.models.user import User
from app.config import settings
from typing import Optional

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = AuthService.create_user(db, user_data.email, user_data.password, user_data.full_name)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = AuthService.create_access_token(str(user.id))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRATION_HOURS * 3600
    }


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> uuid_module.UUID:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    user_id_str = AuthService.verify_token(token)
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        uuid_obj = uuid_module.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == uuid_obj).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return uuid_obj


@router.get("/me", response_model=UserResponse)
async def get_me(user_id: uuid_module.UUID = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
