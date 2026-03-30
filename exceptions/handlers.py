import inspect
import logging
import sys

from fastapi import FastAPI
from jwt import InvalidTokenError
from sqlalchemy.util import has_dupes
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from starlette.requests import Request
from starlette.responses import JSONResponse

from exceptions.customExceptions import NotFoundException, ResourceAlreadyExistsException, ForbiddenException

logger = logging.getLogger()

def handledException(ex : type[Exception]):
    def decorator(func):
        func.ex = ex
        return func
    return decorator


def registerAllExceptionHandlers(app: FastAPI) -> None:
    thisModule = sys.modules[__name__]
    handlers = inspect.getmembers(thisModule, inspect.isfunction)

    for name, handler in handlers:
        if name == "handledException" or name == "registerAllHandlers":
            continue

        try:
            app.add_exception_handler(handler.ex, handler)
        except Exception as e:
            logger.warning(f"handlers should be annotated with 'handledException' to be automatically registered: {name}")
            continue


@handledException(NotFoundException)
def not_found_exception_handler(request: Request, exception: NotFoundException):
    return JSONResponse(status_code= HTTP_404_NOT_FOUND, content= {"message": f"requested {exception.notFoundTarget} not found"})

@handledException(ResourceAlreadyExistsException)
def resource_already_exists_exception_handler(request: Request, exception: ResourceAlreadyExistsException):
    return JSONResponse(status_code= HTTP_409_CONFLICT, content= {"message": f"a resource of type {exception.resourceName} with value {exception.resourceValue} already exists"})

@handledException(InvalidTokenError)
def invalid_token_exception_handler(request: Request, exception: InvalidTokenError):
    return JSONResponse(status_code= HTTP_401_UNAUTHORIZED, content= {"message": "invalid JWT token"})

@handledException(ForbiddenException)
def forbidden_exception_handler(request: Request, exception: ForbiddenException):
    return JSONResponse(status_code = HTTP_403_FORBIDDEN, content= {"message": f"access denied to resource, with cause: {exception.cause}"})
