import os
from fastapi import Depends, FastAPI, Header, HTTPException, status
from services.common.logging import get_logger

API_KEY = os.environ.get("API_KEY", "dev-key")
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN", "dev-token")


def verify_credentials(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> None:
    """Validate the incoming request contains proper auth headers.

    Accepts either an exact `X-API-Key` match or an `Authorization` header
    with a bearer token that matches the gateway's configured token.
    Raises:
        HTTPException: If neither credential is valid.
    """
    if x_api_key == API_KEY or (
        authorization and authorization == f"Bearer {OAUTH_TOKEN}"
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
    )


logger = get_logger("bike-rental-service")

app = FastAPI(dependencies=[Depends(verify_credentials)])


@app.get("/")
async def root() -> dict[str, str]:
    logger.info("root accessed", extra={"service": "bike_rentals"})
    return {"service": "bike_rentals", "message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
