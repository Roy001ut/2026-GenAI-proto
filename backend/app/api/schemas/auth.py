from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool

    @field_validator('id', mode='before')
    @classmethod
    def uuid_to_str(cls, v):
        return str(v)

    model_config = {"from_attributes": True}


class DocumentResponse(BaseModel):
    id: str
    document_type: str
    original_filename: str

    @field_validator('id', mode='before')
    @classmethod
    def uuid_to_str(cls, v):
        return str(v)

    model_config = {"from_attributes": True}
