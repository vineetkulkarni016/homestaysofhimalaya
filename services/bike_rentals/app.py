import os
from io import BytesIO
from datetime import date
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from PIL import Image

try:
    import pytesseract  # type: ignore
except Exception:  # pragma: no cover - optional OCR
    pytesseract = None

from services.common.logging import get_logger

logger = get_logger("bike-rentals-service")
app = FastAPI()

# In-memory data stores
bikes = [
    {"id": 1, "model": "Hero Splendor", "available": True},
    {"id": 2, "model": "Bajaj Pulsar", "available": True},
]
bookings: dict[int, dict] = {}


@app.get("/")
async def root():
    """Service heartbeat."""
    logger.info("root accessed", extra={"service": "bike-rentals"})
    return {"service": "bike-rentals", "message": "Hello World"}


@app.get("/availability")
async def check_availability():
    """Return currently available bikes."""
    return {"available_bikes": [b for b in bikes if b["available"]]}


class BookingRequest(BaseModel):
    user_id: int
    bike_id: int
    start_date: date
    end_date: date


@app.post("/book")
async def book_bike(request: BookingRequest):
    """Book a bike if available."""
    for bike in bikes:
        if bike["id"] == request.bike_id and bike["available"]:
            booking_id = len(bookings) + 1
            bookings[booking_id] = {
                "user_id": request.user_id,
                "bike_id": request.bike_id,
                "start_date": request.start_date,
                "end_date": request.end_date,
                "returned": False,
            }
            bike["available"] = False
            logger.info("bike booked", extra={"booking_id": booking_id})
            return {"booking_id": booking_id}
    raise HTTPException(status_code=404, detail="Bike not available")


class ReturnRequest(BaseModel):
    booking_id: int


@app.post("/return")
async def return_bike(request: ReturnRequest):
    """Mark a bike as returned."""
    booking = bookings.get(request.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking["returned"]:
        raise HTTPException(status_code=400, detail="Bike already returned")
    booking["returned"] = True
    for bike in bikes:
        if bike["id"] == booking["bike_id"]:
            bike["available"] = True
            break
    logger.info("bike returned", extra={"booking_id": request.booking_id})
    return {"status": "returned"}


s3_client = boto3.client("s3")
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "bike-rentals-dev")


async def _process_document(file: UploadFile, name: str) -> dict:
    content = await file.read()
    key = f"{name}/{file.filename}"
    try:
        s3_client.put_object(Bucket=S3_BUCKET, Key=key, Body=content)
    except (BotoCoreError, NoCredentialsError) as exc:  # pragma: no cover
        logger.error("s3 upload failed", extra={"error": str(exc)})
        raise HTTPException(status_code=500, detail="Upload failed")

    manual_review = False
    text = ""
    try:
        if pytesseract:
            image = Image.open(BytesIO(content))
            text = pytesseract.image_to_string(image)
            if not text.strip():
                manual_review = True
        else:
            manual_review = True
    except Exception:  # pragma: no cover - OCR failures
        manual_review = True

    return {
        "document": name,
        "s3_key": key,
        "text": text.strip(),
        "manual_review": manual_review,
    }


@app.post("/documents/upload")
async def upload_documents(
    driving_license: UploadFile = File(...),
    aadhar_card: UploadFile = File(...),
):
    """Upload and validate required documents."""
    results = []
    for doc, name in ((driving_license, "driving_license"), (aadhar_card, "aadhar_card")):
        results.append(await _process_document(doc, name))
    return {"documents": results}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
