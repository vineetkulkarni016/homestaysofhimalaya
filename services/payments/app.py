from fastapi import FastAPI
from services.common.logging import get_logger

logger = get_logger("payment-service")

app = FastAPI()

@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "payment"})
    return {"service": "payment", "message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
