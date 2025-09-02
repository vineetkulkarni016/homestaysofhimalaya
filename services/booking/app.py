from fastapi import FastAPI
from services.common.logging import get_logger

logger = get_logger("booking-service")

app = FastAPI()

@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "booking"})
    return {"service": "booking", "message": "Hello World"}


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
