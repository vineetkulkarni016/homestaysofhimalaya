from fastapi import FastAPI
from pydantic import BaseModel
from services.common.logging import get_logger

logger = get_logger("payment-service")

app = FastAPI()

@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "payment"})
    return {"service": "payment", "message": "Hello World"}


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
