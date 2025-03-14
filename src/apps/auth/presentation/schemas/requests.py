from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(LoginRequest):
    email: EmailStr | None = None


class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


