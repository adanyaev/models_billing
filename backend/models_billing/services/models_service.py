from datetime import timedelta

from sqlalchemy.orm import Session
from sqlalchemy import select
from redis import Redis
from rq import Queue

from models_billing.core.config import Configs
from models_billing.core import exceptions
from models_billing import schemas, models
from models_billing.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from models_billing.inference_queue.task import inference_model_task


redis_conn = Redis(host='redis', port=Configs.REDIS_PORT)
#redis_conn = Redis.from_url(Configs.REDIS_SERVER)

# Создание объекта очереди
queue = Queue(connection=redis_conn)

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
    
    queue.enqueue(inference_model_task, kwargs={'model_id': model.id,
                                                 'inf_request_id': inf_request.id,
                                                 'data': list(request_fields.values())}) # TODO: check field names
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
        return request.inference_result # TODO: add check if exists
    return None
