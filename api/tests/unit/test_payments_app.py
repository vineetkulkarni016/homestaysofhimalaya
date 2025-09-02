import logging
import asyncio


def test_payments_root_endpoint_and_logging(payments_module, caplog):
    app = payments_module.app
    routes = [route.path for route in app.routes]
    assert "/" in routes
    with caplog.at_level(logging.INFO):
        result = asyncio.run(payments_module.root())
    assert result == {"service": "payment", "message": "Hello World"}
    assert any(record.message == "root accessed" and getattr(record, "service", None) == "payment" for record in caplog.records)
