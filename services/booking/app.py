from fastapi import Depends, FastAPI
from services.common.logging import get_logger
from services.common.auth import verify_token
from services.common.http import get as safe_get

from . import models
from .database import SessionLocal, engine
from .tasks import example_booking_task

logger = get_logger("booking-service")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "booking"})
    return {"service": "booking", "message": "Hello World"}



@app.get("/secure")
async def secure(user: str = Depends(verify_token)):
    return {"user": user}


@app.get("/external")
def external_call():
    response = safe_get("https://example.com")
    return {"status": response.status_code}


@app.post("/async-task")
def run_async_task():
    example_booking_task.delay()
    return {"status": "queued"}

@app.get("/itinerary/{booking_id}")
async def get_itinerary(booking_id: int):
    """Return a mock itinerary for the given booking."""
    logger.info("itinerary requested", extra={"service": "booking"})
    itinerary = [
        {"day": 1, "activity": "Check-in"},
        {"day": 2, "activity": "Explore local area"},
    ]
    return {"booking_id": booking_id, "itinerary": itinerary}


@app.get("/history/{user_id}")
async def booking_history(user_id: int):
    """Return a mock booking history for the given user."""
    logger.info("history requested", extra={"service": "booking"})
    history = [
        {"booking_id": 1, "status": "completed"},
        {"booking_id": 2, "status": "upcoming"},
    ]
    return {"user_id": user_id, "bookings": history}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
