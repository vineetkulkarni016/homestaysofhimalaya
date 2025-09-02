import asyncio


def test_service_integration(booking_module, users_module, payments_module, packages_module):
    booking_routes = [route.path for route in booking_module.app.routes]
    users_routes = [route.path for route in users_module.app.routes]
    payments_routes = [route.path for route in payments_module.app.routes]
    packages_routes = [route.path for route in packages_module.app.routes]
    assert "/" in booking_routes
    assert "/" in users_routes
    assert "/" in payments_routes
    assert "/" in packages_routes
    booking_result = asyncio.run(booking_module.root())
    users_result = asyncio.run(users_module.root())
    payments_result = asyncio.run(payments_module.root())
    packages_result = asyncio.run(packages_module.root())
    assert booking_result["service"] == "booking"
    assert users_result["service"] == "user"
    assert payments_result["service"] == "payment"
    assert packages_result["service"] == "packages"
