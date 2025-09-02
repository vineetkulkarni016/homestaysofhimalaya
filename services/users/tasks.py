from services.common.celery_app import celery_app


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def example_user_task(self):
    return "user processed"
