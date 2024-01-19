from datetime import timedelta

from sqlalchemy.orm import Session
from sqlalchemy import select


from models_billing.core import exceptions
from models_billing import schemas, models
from models_billing.core.config import configs
from models_billing.core.security import create_access_token, get_password_hash, verify_password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump(exclude_none=True), is_active=True, is_superuser=False)
    db_user.password = get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    delattr(db_user, "password")
    return db_user


def sign_in_user(db: Session, sign_in_info: schemas.SignIn) -> schemas.SignInResult:
    
    user = get_user_by_email(db, sign_in_info.email)
    if not user:
        raise exceptions.AuthError(detail="Incorrect email or password")
    if not user.is_active:
        raise exceptions.AuthError(detail="Account is not active")
    if not verify_password(sign_in_info.password, user.password):
        raise exceptions.AuthError(detail="Incorrect email or password")
    delattr(user, "password")
    payload = schemas.Payload(
        id=user.id,
        email=user.email,
        is_superuser=user.is_superuser,
    )
    token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
    sign_in_result = {
        "access_token": access_token,
        "expiration": expiration_datetime,
        "user_info": user,
    }
    return sign_in_result
