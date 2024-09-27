from typing import Any, Callable, Awaitable
import math
import re

from http import HTTPStatus
import json
from urllib.parse import parse_qs

from utils import reply, reply_bad_request, reply_unprocessable_entity, reply_not_found


async def application(scope: dict[str, Any],
                      receive: Callable[[], Awaitable[dict[str, Any]]],
                      send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
    assert scope["type"] == "http"
    method = scope["method"]
    path = scope["path"]

    if method != "GET":
        await reply_not_found(send)
        return

    params = parse_qs(scope["query_string"].decode())

    if path == "/factorial":
        n = params.get("n")
        if n is None or len(n) != 1 or not re.match(r"^[+-]?[0-9]+$", n[0]):
            await reply_unprocessable_entity(send)
            return

        n = int(n[0])
        if n < 0:
            await reply_bad_request(send)
            return

        await reply(send,
                    HTTPStatus.OK,
                    [("Content-Type", "application/json")],
                    json.dumps({"result": math.factorial(n)}))

    elif re.match("^/fibonacci/[^/]*$", path):
        if not re.match(r"^/fibonacci/-?\d+$", path):
            await reply_unprocessable_entity(send)
            return

        n = int(path.split("/")[2])
        if n < 0:
            await reply_bad_request(send)
            return

        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        await reply(send,
                    HTTPStatus.OK,
                    [("Content-Type", "application/json")],
                    json.dumps({"result": a}))

    elif path == "/mean":
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            body += message["body"]
            more_body = message.get("more_body", False)

        body = body.decode()
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            await reply_unprocessable_entity(send)
            return

        if not isinstance(body, list) or not all(isinstance(x, (int, float)) for x in body):
            await reply_unprocessable_entity(send)
            return

        if not body:
            await reply_bad_request(send)
            return

        await reply(send,
                    HTTPStatus.OK,
                    [("Content-Type", "application/json")],
                    json.dumps({"result": sum(body) / len(body)}))
    else:
        await reply_not_found(send)
