from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from models_billing.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    balance = Column(Integer, default=1000)
    inf_requests = relationship("InferenceRequest", back_populates="user")


class MlModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Integer, default=100)
    description = Column(String)
    inf_requests = relationship("InferenceRequest", back_populates="model")


class InferenceRequest(Base):
    __tablename__ = "inference_request"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(Integer, default=0)

    cost = Column(Integer, default=100)

    result = Column(Float, default=None)

    model_id = Column(Integer, ForeignKey("ml_models.id"))

    model = relationship("MlModel", back_populates="inf_requests")

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="inf_requests")
