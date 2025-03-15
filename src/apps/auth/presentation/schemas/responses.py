import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserNotFoundResponse(BaseModel):
    user_id: uuid.UUID
    username: str


class RegisterResponse(BaseModel):
    username: str
    access_jwt: str


class LoginResponse(BaseModel):
    access_jwt: str


class GetMeResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str | None


class RefreshAccessJwtResponse(BaseModel):
    access_jwt: str




