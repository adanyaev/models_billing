from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models_billing.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    balance: Mapped[int] = mapped_column(Integer, default=1000)
    inf_requests: Mapped[list["InferenceRequest"]] = relationship("InferenceRequest", back_populates="user")


class MlModel(Base):
    __tablename__ = "ml_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    price: Mapped[int] = mapped_column(Integer, default=100)
    description: Mapped[str] = mapped_column(String)
    inf_requests: Mapped[list["InferenceRequest"]] = relationship("InferenceRequest", back_populates="model")
    weights_path: Mapped[str] = mapped_column(String, unique=True)

class InferenceRequest(Base):
    __tablename__ = "inference_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    #SEQN, age_group, RIDAGEYR, RIAGENDR, PAQ605, BMXBMI, LBXGLU, DIQ010, LBXGLT, LBXIN

    SEQN: Mapped[float] = mapped_column(Float)
    RIAGENDR: Mapped[float] = mapped_column(Float)
    PAQ605: Mapped[float] = mapped_column(Float)
    BMXBMI: Mapped[float] = mapped_column(Float)
    LBXGLU: Mapped[float] = mapped_column(Float)
    DIQ010: Mapped[float] = mapped_column(Float)
    LBXGLT: Mapped[float] = mapped_column(Float)
    LBXIN: Mapped[float] = mapped_column(Float)

    status: Mapped[int] = mapped_column(Integer, default=0)

    cost: Mapped[int] = mapped_column(Integer, default=100)

    model_id: Mapped[int] = mapped_column(Integer, ForeignKey("ml_models.id"))

    model: Mapped['MlModel'] = relationship("MlModel", back_populates="inf_requests")

    user_id : Mapped[int]= mapped_column(Integer, ForeignKey("users.id"))

    user: Mapped['User'] = relationship("User", back_populates="inf_requests")

    inference_result: Mapped['InferenceResult'] = relationship("InferenceResult", back_populates="inference_request")


class InferenceResult(Base):
    __tablename__ = "inference_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    value: Mapped[str] = mapped_column(String)

    inference_request_id: Mapped[int] = mapped_column(Integer, ForeignKey("inference_requests.id"))

    inference_request: Mapped['InferenceRequest'] = relationship("InferenceRequest", back_populates="inference_result")
    