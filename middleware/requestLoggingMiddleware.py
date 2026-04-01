import uuid
import logging
from typing import Dict

from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware, _StreamingResponse
from starlette.requests import Request


def _getHeaderString(headers:  Headers) -> str:
    string = ""
    for key, value in headers.items():
        string += f"\n {key}: {value} "
    return string


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger("RequestLogger")
        message = f"""incoming request with URL: {request.url} method: {request.method} and headers: {_getHeaderString(request.headers)}"""

        if request.method in ("POST", "PUT", "PATCH"):
            message += f"\nbody: {await request.body()} "

        requestId  = str(uuid.uuid4())
        message += f"\nassigned request id: {requestId}"
        request.state.requestId = requestId

        logger.info(message)

        response = await call_next(request)

        logger.info(f"request with id: {request.state.requestId} generated response with status code: {response.status_code}")
        logger.warning("im aware that some headers should never be printed (e.g. authorization), but this is just and exercise")

        return response