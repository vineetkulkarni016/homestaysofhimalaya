import logging
import asyncio


def test_booking_user_and_payments_services_integration(booking_module, users_module, payments_module, caplog):
    booking_routes = [route.path for route in booking_module.app.routes]
    users_routes = [route.path for route in users_module.app.routes]
    payments_routes = [route.path for route in payments_module.app.routes]
    assert "/" in booking_routes
    assert "/" in users_routes
    assert "/" in payments_routes
    with caplog.at_level(logging.INFO):
        booking_result = asyncio.run(booking_module.root())
        users_result = asyncio.run(users_module.root())
        payments_result = asyncio.run(payments_module.root())
    assert booking_result["service"] == "booking"
    assert users_result["service"] == "user"
    assert payments_result["service"] == "payment"
    services_logged = {getattr(record, "service", None) for record in caplog.records if record.message == "root accessed"}
    assert services_logged == {"booking", "user", "payment"}
