#  ruff: noqa: S101, N802
from typing import Any

from src.loamy.session import RequestMap


def test_valid_RequestMap(base_config: dict[str, Any]):
    req_map = RequestMap(
        url=base_config["url"],
        http_op="GET",
        body=base_config["body"],
        query_params=base_config["queryParams"],
        headers=base_config["headers"],
    )
    assert req_map.url == base_config["url"]
    assert req_map.http_op == "GET"
    assert req_map.body == base_config["body"]
    assert req_map.query_params == base_config["queryParams"]
    assert req_map.headers == base_config["headers"]
