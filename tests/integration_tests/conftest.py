from collections.abc import Callable

import pytest
import requests

from tests.integration_tests.helpers import API_URL


@pytest.fixture
def products() -> dict[str, str]:
    products_response = requests.get(f"{API_URL}/products")
    assert products_response.ok
    return {
        product["product_type"]: product["product_id"]
        for product in (products_response.json())
    }


@pytest.fixture
def get_subscriptions() -> Callable:
    def get() -> dict[str, str]:
        subscriptions_response = requests.get(f"{API_URL}/subscriptions/all")
        assert subscriptions_response.ok
        return {sub["subscription_id"]: sub for sub in (subscriptions_response.json())}

    return get


@pytest.fixture
def get_workflows() -> Callable:
    def get() -> dict[str, str]:
        subscriptions_response = requests.get(f"{API_URL}/subscriptions/all")
        assert subscriptions_response.ok
        return {sub["subscription_id"]: sub for sub in (subscriptions_response.json())}

    return get


@pytest.fixture(autouse=True)
def clean(get_subscriptions):
    yield

    for sub_id, _ in get_subscriptions().items():
        assert requests.delete(f"{API_URL}/subscriptions/{sub_id}").ok
