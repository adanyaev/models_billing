from pydantic import BaseModel
from datetime import datetime

class InferenceRequestBase(BaseModel):
    pass


class InferenceRequestCreate(InferenceRequestBase):
    pass

class InferenceRequestGet(InferenceRequestBase):
    pass


class InferenceRequest(InferenceRequestBase):
    id: int

    status: int
    cost: int
    result: float | None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    balance: int

    inf_requests: list[InferenceRequest]

    class Config:
        orm_mode = True


class SignIn(BaseModel):
    email: str
    password: str


class SignInResult(BaseModel):
    access_token: str
    expiration: datetime
    user_info: User


class Payload(BaseModel):
    id: int
    email: str
    is_superuser: bool