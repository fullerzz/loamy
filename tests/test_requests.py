import pytest

from src.loamy.session import Clump, RequestMap, RequestResponse


@pytest.fixture(scope="session")
def request_map_collection() -> list[RequestMap]:
    requests: list[RequestMap] = []
    for i in range(0, 100):
        print(i)
        if i % 2 == 0:
            requests.append(
                RequestMap(
                    url="http://localhost:44777/",
                    httpOperation="GET",
                )
            )
        else:
            requests.append(
                RequestMap(
                    url="http://localhost:44777/foo",
                    httpOperation="POST",
                    body={"foo": "bar"},
                )
            )
    return requests


@pytest.fixture(scope="session")
def request_map_to_trigger_exception() -> RequestMap:
    return RequestMap(
        url="http://localhost:44777/exception",
        httpOperation="GET",
    )


def test_send_requests(request_map_collection: list[RequestMap]) -> None:
    session = Clump(requests=request_map_collection)
    responses: list[RequestResponse] = session.sendRequests()
    assert len(responses) == 100
    for response in responses:
        assert response.statusCode == 200
        assert response.error is None


def test_send_requests_with_exceptions(
    request_map_collection: list[RequestMap],
    request_map_to_trigger_exception: RequestMap,
) -> None:
    requests: list[RequestMap] = request_map_collection.copy()
    requests.append(request_map_to_trigger_exception)
    session = Clump(requests=requests)
    responses: list[RequestResponse] = session.sendRequests(return_exceptions=True)
    assert len(responses) == 101
    for response in responses:
        if response.requestMap.url == "http://localhost:44777/exception":
            assert response.statusCode == 0
            assert response.error is not None
        else:
            assert response.statusCode == 200
            assert response.error is None
