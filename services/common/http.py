import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import pybreaker

breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)


@breaker
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def get(url: str, **kwargs):
    return requests.get(url, **kwargs)
