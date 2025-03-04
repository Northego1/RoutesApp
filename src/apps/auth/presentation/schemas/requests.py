from pydantic import BaseModel, EmailStr


class LoginRequestSchema(BaseModel):
    username: str
    password: str


class RegisterRequestSchema(LoginRequestSchema):
    email: EmailStr


class UpdateUserRequestSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
