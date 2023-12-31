![CI Workflow](https://github.com/fullerzz/zConcurrent/actions/workflows/ci.yml/badge.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

# Overview

This project allows you to execute a list of http operations asynchronously from within an synchronous context.

It does not care whether you should do this. It simply allows you to do so if you desire.

## Installing

The package is available via pip.

```bash
pip install loamy
```

If you're not on Windows, install the uvloop extra to increase performance.

```bash
pip install "loamy[uvloop]"
```

## Usage

The package can be imported as shown:

```python
from loamy.session import Clump, RequestMap, RequestResponse
```

| Class | Description|
| ----- | -----------|
| `Clump` | Container object that stores collection of requests (type RequestMap) to send |
| `RequestMap` | Container object that stores all info about an individual request to send |
| `RequestResponse` | Container object that stores the request response and any exception raised for each individual request |


### Example

```python
# Create RequestMap objects
req1 = RequestMap(
    url="https://baconipsum.com/api",
    httpOperation="GET",
    queryParams={"type": "meat-and-filler", "format": "json"},
)
req2 = RequestMap(
    url="https://baconipsum.com/api",
    httpOperation="GET",
    queryParams={"type": "all-meat", "format": "json"},
)
req3 = RequestMap(
    url="https://baconipsum.com/api",
    httpOperation="GET",
    queryParams={"type": "meat-and-filler", "format": "json"},
)

# Create Clump and call sendRequests()
session = Clump(requests=[req1, req2, req3])
responses: list[RequestResponse] = session.sendRequests(return_exceptions=True)


# Handle responses for individual requests
for resp in responses:
    httpVerb = resp.requestMap.httpOperation
    print(f"Evaluating response for {httpVerb} request to {resp.requestMap.url}")
    if resp.error is not None:
        print("Exception raised for request")
    else:
        print(f"Status Code: {resp.statusCode}")
        if resp.body is not None:
            print(resp.body)
```

#### RequestMap Class

```python
class RequestMap(msgspec.Struct):
    url: str
    httpOperation: Literal["GET", "POST", "PUT", "PATCH", "OPTIONS", "DELETE"]
    body: dict | None = None
    queryParams: dict[str, str] | None = None
    headers: dict[str, str] | None = None
```


#### RequestResponse Class

```python
class RequestResponse(msgspec.Struct):
    requestMap: RequestMap
    statusCode: int
    body: dict | None = None
    error: BaseException | None = None
```
