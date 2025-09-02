import logging
import asyncio


def test_packages_root_endpoint_and_logging(packages_module, caplog):
    app = packages_module.app
    routes = [route.path for route in app.routes]
    assert "/" in routes
    with caplog.at_level(logging.INFO, logger=packages_module.logger.name):
        result = asyncio.run(packages_module.root())
    assert result == {"service": "packages", "message": "Hello World"}


def test_package_list_and_recommendations(packages_module):
    packages = asyncio.run(packages_module.list_packages())
    assert isinstance(packages, list)
    recs = asyncio.run(packages_module.recommendations())
    assert "recommendations" in recs
