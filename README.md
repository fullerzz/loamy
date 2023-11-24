![CI Workflow](https://github.com/fullerzz/zConcurrent/actions/workflows/ci.yml/badge.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

# Overview

This project allows you to execute a list of http operations asynchronously from within an synchronous context.

It does not care whether you should do this. It simply allows you to do so if you desire.

## Installing

The package is available via pip.

```bash
pip install zconcurrent
```

If you're not on Windows, install the uvloop extra to increase performance.

```bash
pip install "zconcurrent[uvloop]"
```

## Usage

The package can be imported as shown:

```python
from zconcurrent.zsession import zSession, RequestMap, RequestResults
```

| Class | Description|
| ----- | -----------|
| `zSession` | Session object containing collection of requests to send |
| `RequestMap` | Container object that stores all info about an individual request to send |
| `RequestResults` | Container object that stores the request responses and any exceptions raised |


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

# Create zSession and call sendRequests()
session = zSession(requestMaps=[req1, req2, req3])
reqResps: RequestResults = session.sendRequests(return_exceptions=True)

# Handle exceptions raised for individual requests
if len(reqResps.taskExceptions) > 0:
    print("Handling exceptions")

# Handle responses for individual requests
for resp in requestResponses:
    httpVerb = resp.requestMap.httpOperation
    print(f"Evaluating response for {httpVerb} request to {resp.requestMap.url}")
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
```

#### RequestResults Class

```python
@dataclass
class RequestResults:
    requestResponses: list[RequestResponse]
    taskExceptions: list[BaseException]
```
