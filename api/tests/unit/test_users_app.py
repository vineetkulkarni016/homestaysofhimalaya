import logging
import asyncio


def test_users_root_endpoint_and_logging(users_module, caplog):
    app = users_module.app
    routes = [route.path for route in app.routes]
    assert "/" in routes
    with caplog.at_level(logging.INFO):
        result = asyncio.run(users_module.root())
    assert result == {"service": "user", "message": "Hello World"}
    assert any(record.message == "root accessed" and getattr(record, "service", None) == "user" for record in caplog.records)
