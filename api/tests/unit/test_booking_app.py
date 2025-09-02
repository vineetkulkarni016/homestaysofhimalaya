import logging
import asyncio


def test_booking_root_endpoint_and_logging(booking_module, caplog):
    app = booking_module.app
    routes = [route.path for route in app.routes]
    assert "/" in routes
    with caplog.at_level(logging.INFO):
        result = asyncio.run(booking_module.root())
    assert result == {"service": "booking", "message": "Hello World"}
    assert any(record.message == "root accessed" and getattr(record, "service", None) == "booking" for record in caplog.records)
