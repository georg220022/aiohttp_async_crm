import base64
from typing import Any, Optional
from aiohttp.web_response import Response
from aiohttp.web import json_response as aiohttp_json_response


def json_response(data: Any = None, status: str = "ok") -> Response:
    if data is None:
        data = dict()
    return aiohttp_json_response(data=dict(status=status, data=data))


def error_json_response(
    http_status: int,
    status: str = "error",
    message: Optional[str] = "",
    data: Optional[dict] = None,
):
    if data is None:
        data = dict()
    return aiohttp_json_response(
        status=http_status, data=dict(status=status, message=message, data=data)
    )


def check_basic_auth(raw_credentials: str, username: str, password: str) -> bool:
    credentials = base64.b64decode(raw_credentials).decode("utf-8")
    parts = credentials.split(":")
    if len(parts) != 2:
        return False
    return parts[0] == username and parts[1] == str(password)
