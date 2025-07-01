from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
