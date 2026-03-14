from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool

    @field_validator("id", mode="before")
    @classmethod
    def coerce_uuid(cls, v):
        return str(v)

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    """Returned by both /login and /register — token + user in one shot."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
