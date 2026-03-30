import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from exceptions.customExceptions import NotFoundException
from exceptions.handlers import registerAllExceptionHandlers
from middleware.requestLoggingMiddleware import RequestLoggingMiddleware
from repository.ormBase import initDb
from routes.testRoute import rt


@asynccontextmanager
async def lifespan(application: FastAPI):
    await initDb()
    yield

logging.basicConfig(level=logging.INFO, format= '%(levelname)s:%(asctime)s - %(name)s -  %(message)s')

app = FastAPI(lifespan = lifespan)

registerAllExceptionHandlers(app)

# middleware section
app.add_middleware(RequestLoggingMiddleware)

# routes
app.include_router(rt)



















