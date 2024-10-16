from typing import Any, Callable, Awaitable, Optional
import json
from http import HTTPStatus


async def reply(send: Callable[[dict[str, Any]], Awaitable[None]],
                status: HTTPStatus,
                headers: Optional[list[tuple[str, str]]] = None,
                body: Optional[str] = None):
    start_data = {
        "type": "http.response.start",
        "status": status,
    }
    if headers is not None:
        for header in headers:
            header = (header[0].encode(), header[1].encode())
        start_data["headers"] = headers
    await send(start_data)

    body_data = {
        "type": "http.response.body",
    }
    if body is not None:
        body_data["body"] = body.encode()
    await send(body_data)


async def reply_not_found(send: Callable[[dict[str, Any]], Awaitable[None]]):
    await reply(send,
                HTTPStatus.NOT_FOUND,
                [("Content-Type", "application/json")],
                json.dumps({"detail": "Not Found"}))


async def reply_unprocessable_entity(send: Callable[[dict[str, Any]], Awaitable[None]]):
    await reply(send,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                [("Content-Type", "application/json")],
                json.dumps({"detail": "Unprocessable Entity"}))


async def reply_bad_request(send: Callable[[dict[str, Any]], Awaitable[None]]):
    await reply(send,
                HTTPStatus.BAD_REQUEST,
                [("Content-Type", "application/json")],
                json.dumps({"detail": "Bad Request"}))
