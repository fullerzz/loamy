from src.zconcurrent.zsession import RequestMap
from typing import Any, Dict


def test_valid_RequestMap(base_config: Dict[str, Any]):
    requestMap = RequestMap(
        url=base_config["url"],
        httpOperation="GET",
        body=base_config["body"],
        queryParams=base_config["queryParams"],
        headers=base_config["headers"],
    )
    assert requestMap.url == base_config["url"]
    assert requestMap.httpOperation == "GET"
    assert requestMap.body == base_config["body"]
    assert requestMap.queryParams == base_config["queryParams"]
    assert requestMap.headers == base_config["headers"]
