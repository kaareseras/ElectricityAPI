from pydantic import EmailStr

from src.fastapi_app.schemas.base import BaseSchema


class RegisterUserRequest(BaseSchema):
    name: str
    email: EmailStr
    password: str


class UpdateUserRequest(BaseSchema):
    name: str
    email: EmailStr


class VerifyUserRequest(BaseSchema):
    token: str
    email: EmailStr


class EmailRequest(BaseSchema):
    email: EmailStr


class ResetRequest(BaseSchema):
    token: str
    email: EmailStr
    password: str
