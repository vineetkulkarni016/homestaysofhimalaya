import logging
import asyncio


def test_booking_root_endpoint_and_logging(booking_module, caplog):
    app = booking_module.app
    routes = [route.path for route in app.routes]
    assert "/" in routes
    with caplog.at_level(logging.INFO, logger=booking_module.logger.name):
        result = asyncio.run(booking_module.root())
    assert result == {"service": "booking", "message": "Hello World"}


def test_itinerary_and_history_endpoints(booking_module):
    itinerary = asyncio.run(booking_module.get_itinerary(1))
    assert itinerary["booking_id"] == 1
    assert isinstance(itinerary["itinerary"], list)
    history = asyncio.run(booking_module.booking_history(99))
    assert history["user_id"] == 99
    assert isinstance(history["bookings"], list)
