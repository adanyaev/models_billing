from datetime import timedelta

from sqlalchemy.orm import Session
from sqlalchemy import select


from models_billing.core import exceptions
from models_billing import schemas, models
from models_billing.core.config import configs
from models_billing.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)

def create_inf_request(db: Session, user_id: int, inference_request_data: schemas.InferenceRequestCreate):

    user = db.scalars(select(models.User).filter(models.User.id == user_id)).first()
    model = db.scalars(select(models.MlModel).filter(models.MlModel.id == inference_request_data.ml_model_id)).first()
    request_fields = inference_request_data.model_dump()
    del request_fields['ml_model_id']
    inf_request = models.InferenceRequest(user=user, model=model, cost=model.price, **request_fields)
    # TODO: add redis add to queue and user balance minus
    db.add(inf_request)
    db.commit()
    db.refresh(inf_request)
    return inf_request


def get_inf_requests(db: Session, user_id: int):
    # stmt = select(models.User).filter(models.User.id == user_id).join(models.User.inf_requests)
    stmt = select(models.InferenceRequest).filter(
        models.InferenceRequest.user_id == user_id
    )
    requests = db.scalars(stmt).all()
    return requests


def get_inf_result(db: Session, user_id: int, request_id: int):

    stmt = select(models.InferenceRequest).filter(
        models.InferenceRequest.user_id == user_id and
        models.InferenceRequest.id == request_id
    )
    request = db.scalars(stmt).first()
    if request:
        # stmt = (
        #     select(models.InferenceResult)
        #     .filter(
        #         models.InferenceResult.inference_request_id == request.id
        #     )
        # )
        # result = db.execute(stmt).first()
        return request.inference_result.first()
    return []
