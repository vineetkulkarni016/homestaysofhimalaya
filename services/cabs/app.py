import os
import json
from math import radians, sin, cos, sqrt, atan2
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import redis.asyncio as redis
from services.common.logging import get_logger

logger = get_logger("cabs-service")

app = FastAPI()

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# simple in-memory stores for demo
DRIVERS = ["driver1", "driver2", "driver3"]
RIDES = {}
COUNTER = 0

GEOFENCE = {
    "lat_min": 28.0,
    "lat_max": 31.0,
    "lon_min": 77.0,
    "lon_max": 80.0,
}

class RideRequest(BaseModel):
    rider_id: str
    pickup_lat: float
    pickup_lon: float
    dropoff_lat: float
    dropoff_lon: float

def is_within_geofence(lat: float, lon: float) -> bool:
    return (
        GEOFENCE["lat_min"] <= lat <= GEOFENCE["lat_max"]
        and GEOFENCE["lon_min"] <= lon <= GEOFENCE["lon_max"]
    )

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def estimate_fare(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    distance = haversine(lat1, lon1, lat2, lon2)
    base_fare = 50
    per_km = 10
    return round(base_fare + per_km * distance, 2)

@app.post("/rides")
async def request_ride(req: RideRequest):
    if not is_within_geofence(req.pickup_lat, req.pickup_lon):
        raise HTTPException(status_code=400, detail="Pickup outside service area")
    global COUNTER
    COUNTER += 1
    driver_id = DRIVERS[COUNTER % len(DRIVERS)]
    ride = {
        "id": COUNTER,
        "rider_id": req.rider_id,
        "driver_id": driver_id,
        "pickup": [req.pickup_lat, req.pickup_lon],
        "dropoff": [req.dropoff_lat, req.dropoff_lon],
        "status": "assigned",
        "fare": None,
    }
    RIDES[COUNTER] = ride
    logger.info("ride_requested", extra={"ride_id": COUNTER, "driver_id": driver_id})
    return ride

@app.get("/rides/{ride_id}")
async def get_ride(ride_id: int):
    ride = RIDES.get(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride

@app.post("/rides/{ride_id}/start")
async def start_ride(ride_id: int):
    ride = RIDES.get(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    ride["status"] = "ongoing"
    return ride

@app.post("/rides/{ride_id}/complete")
async def complete_ride(ride_id: int):
    ride = RIDES.get(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    fare = estimate_fare(
        ride["pickup"][0], ride["pickup"][1], ride["dropoff"][0], ride["dropoff"][1]
    )
    ride["fare"] = fare
    ride["status"] = "completed"
    return ride

@app.websocket("/ws/locations/{driver_id}")
async def location_ws(websocket: WebSocket, driver_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            await redis_client.set(
                f"driver:{driver_id}:location", json.dumps(payload)
            )
            await redis_client.publish(
                "driver_locations", json.dumps({"driver_id": driver_id, **payload})
            )
    except WebSocketDisconnect:
        logger.info("driver_disconnected", extra={"driver_id": driver_id})

@app.get("/")
async def root():
    return {"service": "cabs", "message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
