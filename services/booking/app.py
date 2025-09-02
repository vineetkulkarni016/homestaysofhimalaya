from fastapi import FastAPI
from services.common.logging import get_logger

logger = get_logger("booking-service")

app = FastAPI()

@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "booking"})
    return {"service": "booking", "message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
