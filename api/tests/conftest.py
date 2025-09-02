import importlib.util
import pathlib
import logging
import pytest


def load_service_module(service_name: str):
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    module_path = repo_root / 'services' / service_name / 'app.py'
    spec = importlib.util.spec_from_file_location(f"{service_name}_app", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Remove CloudWatch handlers to avoid external AWS calls during tests
    logger = logging.getLogger()
    for handler in list(logger.handlers):
        if handler.__class__.__name__ == 'CloudWatchLogHandler':
            logger.removeHandler(handler)
    return module


@pytest.fixture(scope="module")
def booking_module():
    return load_service_module('booking')


@pytest.fixture(scope="module")
def users_module():
    return load_service_module('users')


@pytest.fixture(scope="module")
def payments_module():
    return load_service_module('payments')
