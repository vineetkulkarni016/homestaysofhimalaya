from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict
import httpx
import os

from services.common.logging import get_logger

logger = get_logger("hosts-service")
app = FastAPI()

# In-memory store for properties
properties: Dict[int, Dict] = {}
property_counter = 1

class PropertyCreate(BaseModel):
    name: str
    location: str

class InventoryUpdate(BaseModel):
    rooms: int

class PricingUpdate(BaseModel):
    price: float

class AvailabilityUpdate(BaseModel):
    availability: int

def role_required(*roles):
    async def dependency(x_role: str = Header(...)):
        if x_role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
    return dependency

@app.post("/properties", dependencies=[Depends(role_required("manager"))])
async def register_property(payload: PropertyCreate):
    global property_counter
    prop_id = property_counter
    properties[prop_id] = {
        "id": prop_id,
        "name": payload.name,
        "location": payload.location,
        "rooms": 0,
        "price": 0.0,
        "availability": 0,
    }
    property_counter += 1
    logger.info("property registered", extra={"id": prop_id})
    return properties[prop_id]

@app.put("/properties/{prop_id}/inventory", dependencies=[Depends(role_required("manager"))])
async def update_inventory(prop_id: int, payload: InventoryUpdate):
    prop = properties.get(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    prop["rooms"] = payload.rooms
    logger.info("inventory updated", extra={"id": prop_id})
    return prop

@app.put("/properties/{prop_id}/pricing", dependencies=[Depends(role_required("manager"))])
async def update_pricing(prop_id: int, payload: PricingUpdate):
    prop = properties.get(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    prop["price"] = payload.price
    logger.info("pricing updated", extra={"id": prop_id})
    return prop

@app.put("/properties/{prop_id}/availability", dependencies=[Depends(role_required("manager", "receptionist"))])
async def update_availability(prop_id: int, payload: AvailabilityUpdate):
    prop = properties.get(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    prop["availability"] = payload.availability
    logger.info("availability updated", extra={"id": prop_id})
    return prop

@app.get("/properties/{prop_id}/sync", dependencies=[Depends(role_required("manager", "receptionist"))])
async def sync_bookings(prop_id: int):
    """Sync availability with booking service."""
    prop = properties.get(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    booking_url = os.getenv("BOOKING_SERVICE_URL", "http://booking-service:8000")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(booking_url)
            response.raise_for_status()
            data = response.json()
            # Placeholder: update availability from booking data if provided
            if isinstance(data, dict) and "available" in data:
                prop["availability"] = data["available"]
    except Exception as exc:
        logger.warning("booking sync failed", extra={"error": str(exc)})
    return prop

@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "hosts"})
    return {"service": "hosts", "message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
