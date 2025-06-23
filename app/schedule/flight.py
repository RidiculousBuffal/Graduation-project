from app import app,celery

@celery.task
def health_check():
    print("healthy")
    return "healthy"

