import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserNotFoundResponse(BaseModel):
    user_id: uuid.UUID
    username: str


class RegisterResponse(BaseModel):
    username: str
    email: EmailStr


class LoginResponse(BaseModel):
    refresh_jwt: str


class GetUserResponse(RegisterResponse):
    id: uuid.UUID
    registred_at: datetime


class RefreshAccessJwtResponse(BaseModel):
    access_jwt: str




