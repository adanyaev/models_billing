from pydantic import BaseModel
from datetime import datetime


# class MlModel(BaseModel):
#     pass

# class InferenceResult(BaseModel):
#     pass

class InferenceRequestBase(BaseModel):

    SEQN: float
    RIAGENDR: float
    PAQ605: float
    BMXBMI: float
    LBXGLU: float
    DIQ010: float
    LBXGLT: float
    LBXIN: float
    


class InferenceRequestCreate(InferenceRequestBase):
    ml_model_id: int


class InferenceRequestGet(InferenceRequestBase):
    pass

class MlModel(BaseModel):
    id: int
    name: str
    price: int
    description: str

    class Config:
        orm_mode = True


class InferenceRequest(InferenceRequestBase):
    id: int
    status: int
    cost: int
    # result: InferenceResult | None
    model : MlModel

    class Config:
        orm_mode = True


class InferenceResult(BaseModel):
    id: int 

    value: float

    #inference_request: [InferenceRequest]

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

    #inf_requests: list[InferenceRequest]

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