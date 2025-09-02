from services.common.celery_app import celery_app


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def example_booking_task(self):
    return "booking processed"
