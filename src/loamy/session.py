import asyncio
from json import JSONDecodeError
from typing import Literal

import aiohttp
from loguru import logger
from pydantic import BaseModel, ConfigDict

# Disable the logger. If a consuming app wishes to see loamy's logs, they can enable() it again.
logger.disable("loamy")
# https://loguru.readthedocs.io/en/stable/overview.html#suitable-for-scripts-and-libraries
try:
    import uvloop

    async_run = uvloop.run
    logger.debug("Using uvloop for async operations")
except ModuleNotFoundError:
    async_run = asyncio.run  # type: ignore
    logger.debug("Using asyncio for async operations")


class RequestMap(BaseModel):
    """
    Class containing information about a single HTTP request to be sent.
    """

    url: str
    http_op: Literal["GET", "POST", "PUT", "PATCH", "OPTIONS", "DELETE"]
    body: dict | None = None
    query_params: dict[str, str] | None = None
    headers: dict[str, str] | None = None


class RequestResponse(BaseModel):
    """
    Class containing information about the result of an HTTP request.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    request_map: RequestMap
    status_code: int
    body: dict | None = None
    headers: dict[str, str] | None = None
    error: BaseException | None = None


class Clump:
    """
    Class for sending multiple HTTP requests concurrently.
    """

    def __init__(self, requests: list[RequestMap]) -> None:
        self._requestMaps: list[RequestMap] = requests
        logger.debug(f"Clump created with {len(self._requestMaps)} requests")

    def send_requests(self, return_exceptions: bool = False) -> list[RequestResponse]:
        logger.info(
            f"Sending {len(self._requestMaps)!s} requests with {return_exceptions=!s}"
        )
        return async_run(self._send_requests(rtn_exc=return_exceptions))

    async def _send_requests(self, rtn_exc: bool) -> list[RequestResponse]:
        async with aiohttp.ClientSession() as session:
            http_tasks: list[asyncio.Task] = [
                asyncio.ensure_future(self._route_request(req, session))
                for req in self._requestMaps
            ]
            logger.debug("Beginnging execution of request coroutines")
            results: list[RequestResponse | BaseException] = await asyncio.gather(
                *http_tasks, return_exceptions=rtn_exc
            )
            logger.debug("Finished execution of request coroutines")
            responses: list[RequestResponse] = []
            for i, resp in enumerate(results):
                if isinstance(resp, BaseException):
                    logger.error(f"Manually creating RequestResponse object and nesting error - index {i}")  # fmt: skip
                    responses.append(
                        RequestResponse(
                            request_map=self._requestMaps[i],
                            status_code=418,
                            error=resp,
                        )
                    )
                else:
                    responses.append(resp)
            logger.info(f"Returning {len(responses)!s} responses")
            return responses

    async def _route_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        response: RequestResponse = RequestResponse(request_map=req_map, status_code=0)
        try:
            logger.debug(f"Sending {req_map.http_op} request to {req_map.url}")
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
                    logger.error("No matching HTTP operation found")
                    raise NotImplementedError
        except Exception as e:
            logger.exception(
                f"Error sending {req_map.http_op} request to {req_map.url}"
            )
            response.error = e

        return response

    async def _send_get_request(
        self, req_map: RequestMap, session: aiohttp.ClientSession
    ) -> RequestResponse:
        async with session.get(
            req_map.url, headers=req_map.headers, params=req_map.query_params
        ) as resp:
            error: aiohttp.ContentTypeError | JSONDecodeError | None = None
            status_code: int = resp.status
            logger.debug(f"{resp.url} returned {status_code}")
            try:
                body = await resp.json()
            except (aiohttp.ContentTypeError, JSONDecodeError) as e:
                logger.error(f"Failed to decode JSON response from {resp.url}")
                error = e
                logger.trace("Attempting to read response as text")
                text: str = await resp.text()
                logger.trace("Successfully read response as text")
                body = {"text": text}
        response = RequestResponse(
            request_map=req_map,
            status_code=status_code,
            body=body,
            headers=dict(resp.headers),
            error=error,
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
            error: aiohttp.ContentTypeError | JSONDecodeError | None = None
            status_code: int = resp.status
            logger.debug(f"{resp.url} returned {status_code}")
            try:
                body = await resp.json()
            except (aiohttp.ContentTypeError, JSONDecodeError) as e:
                logger.error(f"Failed to decode JSON response from {resp.url}")
                error = e
                logger.trace("Attempting to read response as text")
                text: str = await resp.text()
                logger.trace("Successfully read response as text")
                body = {"text": text}
        response = RequestResponse(
            request_map=req_map,
            status_code=status_code,
            body=body,
            headers=dict(resp.headers),
            error=error,
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
            error: aiohttp.ContentTypeError | JSONDecodeError | None = None
            logger.debug(f"{resp.url} returned {status_code}")
            try:
                body = await resp.json()
            except (aiohttp.ContentTypeError, JSONDecodeError) as e:
                logger.error(f"Failed to decode JSON response from {resp.url}")
                error = e
                logger.trace("Attempting to read response as text")
                text: str = await resp.text()
                logger.trace("Successfully read response as text")
                body = {"text": text}
        response = RequestResponse(
            request_map=req_map,
            status_code=status_code,
            body=body,
            headers=dict(resp.headers),
            error=error,
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
            error: aiohttp.ContentTypeError | JSONDecodeError | None = None
            logger.debug(f"{resp.url} returned {status_code}")
            try:
                body = await resp.json()
            except (aiohttp.ContentTypeError, JSONDecodeError) as e:
                logger.error(f"Failed to decode JSON response from {resp.url}")
                error = e
                logger.trace("Attempting to read response as text")
                text: str = await resp.text()
                logger.trace("Successfully read response as text")
                body = {"text": text}
        response = RequestResponse(
            request_map=req_map,
            status_code=status_code,
            body=body,
            headers=dict(resp.headers),
            error=error,
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
            error: aiohttp.ContentTypeError | JSONDecodeError | None = None
            logger.debug(f"{resp.url} returned {status_code}")
            try:
                body = await resp.json()
            except (aiohttp.ContentTypeError, JSONDecodeError) as e:
                logger.error(f"Failed to decode JSON response from {resp.url}")
                error = e
                logger.trace("Attempting to read response as text")
                text: str = await resp.text()
                logger.trace("Successfully read response as text")
                body = {"text": text}
        response = RequestResponse(
            request_map=req_map,
            status_code=status_code,
            body=body,
            headers=dict(resp.headers),
            error=error,
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
            error: aiohttp.ContentTypeError | JSONDecodeError | None = None
            logger.debug(f"{resp.url} returned {status_code}")
            try:
                body = await resp.json()
            except (aiohttp.ContentTypeError, JSONDecodeError) as e:
                logger.error(f"Failed to decode JSON response from {resp.url}")
                error = e
                logger.trace("Attempting to read response as text")
                text: str = await resp.text()
                logger.trace("Successfully read response as text")
                body = {"text": text}
        response = RequestResponse(
            request_map=req_map,
            status_code=status_code,
            body=body,
            headers=dict(resp.headers),
            error=error,
        )
        return response
