from pydantic import BaseModel


class LoginRequest(BaseModel):
    account: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    role: str
