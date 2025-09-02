from fastapi import FastAPI
from services.common.logging import get_logger

logger = get_logger("packages-service")

app = FastAPI()


@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "packages"})
    return {"service": "packages", "message": "Hello World"}


@app.get("/packages")
async def list_packages():
    """Return a list of available travel packages."""
    logger.info("packages listed", extra={"service": "packages"})
    return [
        {"id": 1, "name": "Himalayan Adventure"},
        {"id": 2, "name": "Cultural Tour"},
    ]


@app.get("/recommendations")
async def recommendations(user_id: int | None = None):
    """Return recommended package identifiers."""
    logger.info("recommendations requested", extra={"service": "packages"})
    return {"user_id": user_id, "recommendations": [1, 2]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
