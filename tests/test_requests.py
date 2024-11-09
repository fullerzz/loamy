from typing import List

import pytest

from src.loamy.session import Clump, RequestMap, RequestResponse


@pytest.fixture(scope="session")
def request_map_collection() -> List[RequestMap]:
    requests: List[RequestMap] = []
    for i in range(0, 100):
        if i % 2 == 0:
            requests.append(
                RequestMap(
                    url="http://localhost:44777/",
                    http_op="GET",
                )
            )
        else:
            requests.append(
                RequestMap(
                    url="http://localhost:44777/foo",
                    http_op="POST",
                    body={"foo": "bar"},
                )
            )
    return requests


@pytest.fixture(scope="session")
def request_map_to_trigger_exception() -> RequestMap:
    return RequestMap(
        url="http://localhost:44777/exception",
        http_op="GET",
    )


def test_send_requests(request_map_collection: List[RequestMap]) -> None:
    session = Clump(requests=request_map_collection)
    responses: List[RequestResponse] = session.send_requests()
    assert len(responses) == 100
    for response in responses:
        assert response.status_code == 200
        assert response.error is None
        assert response.headers is not None
        assert response.headers["Content-Type"] == "application/json"
        if response.request_map.http_op == "POST":
            assert response.headers is not None
            assert "x-test" in response.headers
            assert "Test" == response.headers["x-test"]


def test_send_requests_with_exceptions(
    request_map_collection: List[RequestMap],
    request_map_to_trigger_exception: RequestMap,
) -> None:
    requests: List[RequestMap] = request_map_collection.copy()
    requests.append(request_map_to_trigger_exception)
    session = Clump(requests=requests)
    responses: List[RequestResponse] = session.send_requests(return_exceptions=True)
    assert len(responses) == 101
    for response in responses:
        if response.request_map.url == "http://localhost:44777/exception":
            assert response.status_code == 500
            assert response.error is not None
        else:
            assert response.status_code == 200
            assert response.error is None
