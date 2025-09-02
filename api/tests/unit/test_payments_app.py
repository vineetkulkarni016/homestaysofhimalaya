import logging
import asyncio


def test_payments_root_endpoint_and_logging(payments_module, caplog):
    app = payments_module.app
    routes = [route.path for route in app.routes]
    assert "/" in routes
    with caplog.at_level(logging.INFO, logger=payments_module.logger.name):
        result = asyncio.run(payments_module.root())
    assert result == {"service": "payment", "message": "Hello World"}


def test_methods_and_payment_processing(payments_module):
    methods = asyncio.run(payments_module.list_methods())
    assert "credit_card" in methods["methods"]
    request = payments_module.PaymentRequest(amount=100, method="credit_card", promo_code="DISCOUNT10")
    result = asyncio.run(payments_module.process_payment(request))
    assert result["amount_charged"] == 90
