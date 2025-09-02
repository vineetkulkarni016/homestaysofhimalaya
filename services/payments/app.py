
from fastapi import Depends, FastAPI


from pydantic import BaseModel

from services.common.logging import get_logger
from services.common.auth import verify_token
from services.common.http import get as safe_get

from . import models
from .database import SessionLocal, engine
from .tasks import example_payment_task

logger = get_logger("payment-service")

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
    logger.info("root accessed", extra={"service": "payment"})
    return {"service": "payment", "message": "Hello World"}


@app.get("/secure")
async def secure(user: str = Depends(verify_token)):
    return {"user": user}


@app.get("/external")
def external_call():
    response = safe_get("https://example.com")
    return {"status": response.status_code}


@app.post("/async-task")
def run_async_task():
    example_payment_task.delay()
    return {"status": "queued"}

class PaymentRequest(BaseModel):
    amount: float
    method: str
    promo_code: str | None = None


@app.get("/methods")
async def list_methods():
    """Return available payment methods."""
    logger.info("methods listed", extra={"service": "payment"})
    return {"methods": ["credit_card", "paypal", "bank_transfer"]}


@app.post("/pay")
async def process_payment(request: PaymentRequest):
    """Process a mock payment applying promo code discounts."""
    logger.info("payment processed", extra={"service": "payment"})
    amount = request.amount
    if request.promo_code == "DISCOUNT10":
        amount *= 0.9
    return {"method": request.method, "amount_charged": amount}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
