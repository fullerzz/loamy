import asyncio
from typing import Literal

import aiohttp
import msgspec

try:
    import uvloop

    async_run = uvloop.run
except ModuleNotFoundError:
    async_run = asyncio.run  # type: ignore


class RequestMap(msgspec.Struct):
    url: str
    http_op: Literal["GET", "POST", "PUT", "PATCH", "OPTIONS", "DELETE"]
    body: dict | None = None
    query_params: dict[str, str] | None = None
    headers: dict[str, str] | None = None


class RequestResponse(msgspec.Struct):
    request_map: RequestMap
    status_code: int
    body: dict | None = None
    error: BaseException | None = None


class Clump:
    def __init__(self, requests: list[RequestMap]) -> None:
        self._requestMaps: list[RequestMap] = requests

    def send_requests(self, return_exceptions: bool = False) -> list[RequestResponse]:
        return async_run(self._send_requests(rtn_exc=return_exceptions))

    async def _send_requests(self, rtn_exc: bool) -> list[RequestResponse]:
        async with aiohttp.ClientSession() as session:
            http_tasks: list[asyncio.Task] = [
                asyncio.ensure_future(self._route_request(req, session))
                for req in self._requestMaps
            ]
            results: list[RequestResponse | BaseException] = await asyncio.gather(
                *http_tasks, return_exceptions=rtn_exc
            )
            responses: list[RequestResponse] = []
            for i, resp in enumerate(results):
                if isinstance(resp, BaseException):
                    responses.append(
                        RequestResponse(
                            request_map=self._requestMaps[i],
                            status_code=418,
                            error=resp,
                        )
                    )
                else:
                    responses.append(resp)
            return responses

    async def _route_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        response: RequestResponse = RequestResponse(request_map=req_map, status_code=0)
        try:
            match req_map.http_op:
                case "GET":
                    response = await self._send_get_request(req_map, session)
                case "POST":
                    response = await self._send_post_request(req_map, session)
                case "PUT":
                    response = await self._send_put_request(req_map, session)
                case "PATCH":
                    response = await self._send_patch_request(req_map, session)
                case "OPTIONS":
                    response = await self._send_options_request(req_map, session)
                case "DELETE":
                    response = await self._send_delete_request(req_map, session)
                case _:
                    pass
        except Exception as e:
            response.error = e

        return response

    async def _send_get_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.get(
            req_map.url, headers=req_map.headers, params=req_map.query_params
        ) as resp:
            status_code: int = resp.status
            body = await resp.json()
        response = RequestResponse(
            request_map=req_map, status_code=status_code, body=body
        )
        return response

    async def _send_post_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.post(
            req_map.url,
            json=req_map.body,
            headers=req_map.headers,
            params=req_map.query_params,
        ) as resp:
            status_code: int = resp.status
            body = await resp.json()
        response = RequestResponse(
            request_map=req_map, status_code=status_code, body=body
        )
        return response

    async def _send_put_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.put(
            req_map.url,
            json=req_map.body,
            headers=req_map.headers,
            params=req_map.query_params,
        ) as resp:
            status_code: int = resp.status
            body = await resp.json()
        response = RequestResponse(
            request_map=req_map, status_code=status_code, body=body
        )
        return response

    async def _send_patch_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.patch(
            req_map.url,
            json=req_map.body,
            headers=req_map.headers,
            params=req_map.query_params,
        ) as resp:
            status_code: int = resp.status
            body = await resp.json()
        response = RequestResponse(
            request_map=req_map, status_code=status_code, body=body
        )
        return response

    async def _send_options_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.options(
            req_map.url,
            json=req_map.body,
            headers=req_map.headers,
            params=req_map.query_params,
        ) as resp:
            status_code: int = resp.status
            body = await resp.json()
        response = RequestResponse(
            request_map=req_map, status_code=status_code, body=body
        )
        return response

    async def _send_delete_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.delete(
            req_map.url,
            json=req_map.body,
            headers=req_map.headers,
            params=req_map.query_params,
        ) as resp:
            status_code: int = resp.status
            body = await resp.json()
        response = RequestResponse(
            request_map=req_map, status_code=status_code, body=body
        )
        return response
