# app/ext/ext_celery.py
from datetime import timedelta

from celery import Celery
from celery import Task


def make_celery(flask_app):
    class ContextTask(Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return super().__call__(*args, **kwargs)

    from app.config import Config
    celery = Celery(
        flask_app.import_name,  # 现在会是 'app'
        broker=Config.broker_url,
        backend=Config.result_backend,
        task_cls=ContextTask
    )
    include = ['app.schedule.flight']
    # 把 Flask 配置合并进 Celery
    celery.conf.update(flask_app.config)
    imports = ['app.schedule.flight', 'app.worker.faceRecognition', 'app.schedule.inspectionDetect']
    beat_schedule = {
        'healthy_task': {
            'task': 'app.schedule.flight.health_check',
            'schedule': timedelta(hours=8),
        },
        "schedule_detect": {
            'task': 'app.schedule.inspectionDetect.detect_images',
            'schedule': timedelta(hours=8)
        }
    }
    celery.conf.update(beat_schedule=beat_schedule, imports=imports, timezone=Config.timezone)
    celery.flask_app = flask_app  # 备用，在 Task 里仍可访问
    return celery
