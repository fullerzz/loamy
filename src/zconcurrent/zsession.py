import asyncio
import aiohttp
import uvloop
import msgspec
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


class RequestMap(msgspec.Struct):
    url: str
    httpOperation: Literal["GET", "POST", "PUT", "PATCH", "OPTIONS", "DELETE"]
    body: Optional[dict] = None
    queryParams: Optional[Dict[str, str]] = None
    headers: Optional[Dict[str, str]] = None


class RequestResponse(msgspec.Struct):
    requestMap: RequestMap
    statusCode: int
    responseBody: Optional[dict] = None


@dataclass
class RequestResults:
    requestResponses: List[RequestResponse]
    taskExceptions: List[BaseException]


class zSession:
    def __init__(self, requestMaps: List[RequestMap]) -> None:
        self._requestMaps: List[RequestMap] = requestMaps

    def sendRequests(self, return_exceptions: bool = False) -> RequestResults:
        return uvloop.run(self._sendRequests(rtn_exc=return_exceptions))

    async def _sendRequests(self, rtn_exc: bool) -> RequestResults:
        async with aiohttp.ClientSession() as session:
            httpTasks: List[asyncio.Task] = []
            for req in self._requestMaps:
                httpTasks.append(
                    asyncio.ensure_future(self._routeIndividualRequest(req, session))
                )
            responses: List[RequestResponse | BaseException] = await asyncio.gather(
                *httpTasks, return_exceptions=rtn_exc
            )
            requestResults: RequestResults = await _processResults(
                taskResults=responses
            )
            return requestResults

    async def _routeIndividualRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        requestResponse: RequestResponse = RequestResponse(
            requestMap=reqMap, statusCode=0
        )
        match reqMap.httpOperation:
            case "GET":
                requestResponse = await self._sendGetRequest(reqMap, session)
            case "POST":
                requestResponse = await self._sendGetRequest(reqMap, session)
            case "PUT":
                requestResponse = await self._sendPutRequest(reqMap, session)
            case "PATCH":
                requestResponse = await self._sendPatchRequest(reqMap, session)
            case "OPTIONS":
                requestResponse = await self._sendOptionsRequest(reqMap, session)
            case "DELETE":
                requestResponse = await self._sendDeleteRequest(reqMap, session)
            case _:
                pass

        return requestResponse

    async def _sendGetRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.get(
            reqMap.url, headers=reqMap.headers, params=reqMap.queryParams
        ) as resp:
            statusCode: int = resp.status
            responseBody = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, responseBody=responseBody
        )
        return reqResponse

    async def _sendPostRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.post(
            reqMap.url,
            json=reqMap.body,
            headers=reqMap.headers,
            params=reqMap.queryParams,
        ) as resp:
            statusCode: int = resp.status
            responseBody = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, responseBody=responseBody
        )
        return reqResponse

    async def _sendPutRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.put(
            reqMap.url,
            json=reqMap.body,
            headers=reqMap.headers,
            params=reqMap.queryParams,
        ) as resp:
            statusCode: int = resp.status
            responseBody = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, responseBody=responseBody
        )
        return reqResponse

    async def _sendPatchRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.patch(
            reqMap.url,
            json=reqMap.body,
            headers=reqMap.headers,
            params=reqMap.queryParams,
        ) as resp:
            statusCode: int = resp.status
            responseBody = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, responseBody=responseBody
        )
        return reqResponse

    async def _sendOptionsRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.options(
            reqMap.url,
            json=reqMap.body,
            headers=reqMap.headers,
            params=reqMap.queryParams,
        ) as resp:
            statusCode: int = resp.status
            responseBody = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, responseBody=responseBody
        )
        return reqResponse

    async def _sendDeleteRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.delete(
            reqMap.url,
            json=reqMap.body,
            headers=reqMap.headers,
            params=reqMap.queryParams,
        ) as resp:
            statusCode: int = resp.status
            responseBody = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, responseBody=responseBody
        )
        return reqResponse


async def _processResults(
    taskResults: List[RequestResponse | BaseException]
) -> RequestResults:
    responses: List[RequestResponse] = []
    taskExceptions: List[BaseException] = []
    for result in taskResults:
        if isinstance(result, BaseException):
            taskExceptions.append(result)
        else:
            responses.append(result)
    return RequestResults(requestResponses=responses, taskExceptions=taskExceptions)
