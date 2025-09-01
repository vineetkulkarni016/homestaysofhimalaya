import logging
from fastapi import FastAPI
from pythonjsonlogger import jsonlogger
import watchtower

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(stream_handler)

try:
    cw_handler = watchtower.CloudWatchLogHandler(log_group="/homestays/services", stream_name="booking-service")
    cw_handler.setFormatter(jsonlogger.JsonFormatter())
    logger.addHandler(cw_handler)
except Exception as e:
    logger.warning("Unable to initialize CloudWatch log handler", extra={"error": str(e)})

app = FastAPI()

@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "booking"})
    return {"service": "booking", "message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
