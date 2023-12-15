import asyncio
from typing import Literal

import aiohttp
import msgspec

try:
    import uvloop

    asyncRun = uvloop.run
except ModuleNotFoundError:
    asyncRun = asyncio.run


class RequestMap(msgspec.Struct):
    url: str
    httpOperation: Literal["GET", "POST", "PUT", "PATCH", "OPTIONS", "DELETE"]
    body: dict | None = None
    queryParams: dict[str, str] | None = None
    headers: dict[str, str] | None = None


class RequestResponse(msgspec.Struct):
    requestMap: RequestMap
    statusCode: int
    body: dict | None = None
    error: BaseException | None = None


class Clump:
    def __init__(self, requests: list[RequestMap]) -> None:
        self._requestMaps: list[RequestMap] = requests

    def sendRequests(self, return_exceptions: bool = False) -> list[RequestResponse]:
        return asyncRun(self._sendRequests(rtn_exc=return_exceptions))

    async def _sendRequests(self, rtn_exc: bool) -> list[RequestResponse]:
        async with aiohttp.ClientSession() as session:
            httpTasks: list[asyncio.Task] = []
            for req in self._requestMaps:
                httpTasks.append(
                    asyncio.ensure_future(self._routeIndividualRequest(req, session))
                )
            responses: list[RequestResponse] = await asyncio.gather(
                *httpTasks, return_exceptions=rtn_exc
            )
            return responses

    async def _routeIndividualRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        requestResponse: RequestResponse = RequestResponse(
            requestMap=reqMap, statusCode=0
        )
        try:
            match reqMap.httpOperation:
                case "GET":
                    requestResponse = await self._sendGetRequest(reqMap, session)
                case "POST":
                    requestResponse = await self._sendPostRequest(reqMap, session)
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
        except Exception as e:
            requestResponse.error = e

        return requestResponse

    async def _sendGetRequest(
        self, reqMap: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.get(
            reqMap.url, headers=reqMap.headers, params=reqMap.queryParams
        ) as resp:
            statusCode: int = resp.status
            body = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, body=body
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
            body = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, body=body
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
            body = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, body=body
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
            body = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, body=body
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
            body = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, body=body
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
            body = await resp.json()
        reqResponse = RequestResponse(
            requestMap=reqMap, statusCode=statusCode, body=body
        )
        return reqResponse
