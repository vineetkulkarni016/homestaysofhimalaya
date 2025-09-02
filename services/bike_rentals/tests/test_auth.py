import pytest
from fastapi import HTTPException
from services.bike_rentals.app import verify_credentials


def test_rejects_requests_without_credentials():
    with pytest.raises(HTTPException) as exc:
        verify_credentials()
    assert exc.value.status_code == 401


def test_accepts_request_with_api_key():
    # Should not raise an exception when correct API key is provided
    verify_credentials(x_api_key="dev-key")
