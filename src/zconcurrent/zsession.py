import asyncio
import aiohttp
import uvloop
import msgspec
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


class zSession:
    def __init__(self, requestMaps: List[RequestMap]) -> None:
        self._requestMaps = requestMaps

    def sendRequests(self) -> List[RequestResponse]:
        return uvloop.run(self._sendRequests())

    async def _sendRequests(self) -> List[RequestResponse]:
        async with aiohttp.ClientSession() as session:
            httpTasks: List[asyncio.Task] = []
            for req in self._requestMaps:
                httpTasks.append(asyncio.ensure_future(self._routeIndividualRequest(req, session)))
            responses: List[RequestResponse] = await asyncio.gather(*httpTasks)
            return responses

    async def _routeIndividualRequest(self, reqMap: RequestMap, session: aiohttp.ClientSession) -> RequestResponse:
        requestResponse: RequestResponse = RequestResponse(requestMap=reqMap, statusCode=0)
        match reqMap.httpOperation:
            case "GET":
                requestResponse = await self._sendGetRequest(reqMap, session)
            case "POST":
                requestResponse = await self._sendGetRequest(reqMap, session)
            case "PUT":
                raise NotImplementedError
            case "PATCH":
                raise NotImplementedError
            case "OPTIONS":
                raise NotImplementedError
            case "DELETE":
                raise NotImplementedError
            case _:
                pass

        return requestResponse

    async def _sendGetRequest(self, reqMap: RequestMap, session: aiohttp.ClientSession) -> RequestResponse:
        async with session.get(reqMap.url, headers=reqMap.headers, params=reqMap.queryParams) as resp:
            print(resp.status)
            statusCode: int = resp.status
            responseBody = await resp.json()
        reqResponse = RequestResponse(requestMap=reqMap, statusCode=statusCode, responseBody=responseBody)
        return reqResponse

    async def _sendPostRequest(self, reqMap: RequestMap, session: aiohttp.ClientSession) -> RequestResponse:
        async with session.post(
            reqMap.url, json=reqMap.body, headers=reqMap.headers, params=reqMap.queryParams
        ) as resp:
            print(resp.status)
            statusCode: int = resp.status
            responseBody = await resp.json()
        reqResponse = RequestResponse(requestMap=reqMap, statusCode=statusCode, responseBody=responseBody)
        return reqResponse
