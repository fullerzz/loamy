from typing import Any

import pytest


@pytest.fixture
def base_config() -> dict[str, Any]:
    return {
        "url": "https://google.com",
        "body": {"data": "content"},
        "queryParams": {"foo": "bar"},
        "headers": {"Authorization": "TOKEN"},
    }
