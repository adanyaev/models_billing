from models_billing import models

models_data = [{'name': 'LogisticRegression',
                'price': 100,
                'description': "Simple Logistic regression",
                'weights_path': "models_billing/inference_queue/models_weights/logreg.pickle"},
                {'name': 'Svm',
                'price': 200,
                'description': "Svm classifier",
                'weights_path': "models_billing/inference_queue/models_weights/svm.pickle"},
                {'name': 'Catboost',
                'price': 500,
                'description': "Catboost gradient boosting",
                'weights_path': "models_billing/inference_queue/models_weights/cb_model.pickle"},]


def populate_db(engine, sessionmaker):
    models.Base.metadata.create_all(bind=engine)
    db = sessionmaker()
    model_objs = [models.MlModel(**m) for m in models_data]
    db.add_all(model_objs)
    db.commit()
    db.close()
    print('asdasd')
    