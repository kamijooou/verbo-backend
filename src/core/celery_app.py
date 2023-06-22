from celery import Celery

celery_app = Celery("NN_queue", broker="redis://localhost:6379/0")

celery_app.conf.task_routes = {"app.worker.NN_celery": "image-process"}
