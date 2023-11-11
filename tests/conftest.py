import pytest
from typing import Any, Dict


@pytest.fixture
def base_config() -> Dict[str, Any]:
    return {
        "url": "https://google.com",
        "body": {"data": "content"},
        "queryParams": {"foo": "bar"},
        "headers": {"Authorization": "TOKEN"},
    }
