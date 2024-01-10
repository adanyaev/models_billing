import pickle

from redis import Redis
from rq import Queue
import numpy as np
from sqlalchemy import select

from models_billing.core.database import SessionLocal, engine
from models_billing import models, schemas
from models_billing.core.config import Configs


db = None
models_pool = {}

def load_env():
    global db
    global models_pool
    db = SessionLocal()
    models_pool = {}
    stmt = select(models.MlModel)
    model_objs = db.scalars(stmt).all()
    for model_obj in model_objs:
        with open(model_obj.weights_path, 'rb') as f:
            model = pickle.load(f)
        models_pool[model_obj.id] = model
    print(models_pool.keys())

# Функция, которая будет выполняться в фоновом режиме
def inference_model_task(model_id: int, inf_request_id: int, data: list):

    pred = models_pool[model_id].predict(np.array(data).reshape(1, -1))
    inf_request = db.scalars(select(models.InferenceRequest).filter(models.InferenceRequest.id == inf_request_id)).first()
    inf_result = models.InferenceResult(value=str(pred[0]))
    inf_request.inference_result = inf_result
    #inf_request.inference_result.append(inf_result)
    db.commit()
    return
