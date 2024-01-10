from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import  HTTPBearer
from sqlalchemy.orm import Session
from models_billing.core import security
from . import models, schemas
from .services import user_service, models_service
from .core.database import SessionLocal, engine


bearer = security.JWTBearer()

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sign_up/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)


@app.post("/sign_in/", response_model=schemas.SignInResult)
def sign_in_user(sign_in_info: schemas.SignIn, db: Session = Depends(get_db)):
    
    return user_service.sign_in_user(db=db, sign_in_info=sign_in_info)


@app.post("/infer_model/", response_model=schemas.InferenceRequest)
def infer_model(inference_request: schemas.InferenceRequestCreate, token: str = Depends(bearer), db: Session = Depends(get_db)):
    payload = security.decode_jwt(token)
    user_id = payload.get('id')
    return models_service.create_inf_request(db=db, user_id=user_id, inference_request_data=inference_request)


@app.get("/get_inf_requests/", response_model=list[schemas.InferenceRequest])
def get_inf_requests(token: str = Depends(bearer), db: Session = Depends(get_db)):
    payload = security.decode_jwt(token)
    user_id = payload.get('id')
    
    return models_service.get_inf_requests(db, user_id)


@app.get("/get_inf_result/{request_id}", response_model=schemas.InferenceResult)
def get_inf_result(request_id: int, token: str = Depends(bearer), db: Session = Depends(get_db)):
    payload = security.decode_jwt(token)
    user_id = payload.get('id')
    return models_service.get_inf_result(db, user_id, request_id)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
