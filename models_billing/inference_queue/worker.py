
import os

import sklearn
import numpy as np
import catboost
from rq import Worker, Queue, Connection, SimpleWorker
from redis import Redis
from sqlalchemy.orm import Session
from sqlalchemy import select

from models_billing.core.database import SessionLocal, engine
from models_billing import models, schemas

from models_billing.inference_queue.task import load_env, inference_model_task


REDIS_PORT = int(os.getenv("REDIS_PORT", '230231713'))
#REDIS_SERVER: str = os.getenv("REDIS_SERVER", '2313312')

#print(models_pool.keys())
# Подключение к Redis серверу
redis_conn = Redis(host='redis', port=int(REDIS_PORT))
#redis_conn = Redis.from_url(REDIS_SERVER)


# Создание объекта очереди
queue = Queue(connection=redis_conn)

# Создание объекта рабочего процесса
worker = SimpleWorker([queue], connection=redis_conn)

# Запуск рабочего процесса для обработки задач
if __name__ == '__main__':
    load_env()
    worker.work()
