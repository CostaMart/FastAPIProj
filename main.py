import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from middleware.requestLoggingMiddleware import RequestLoggingMiddleware
from routes.testRoute import rt
from security.authentication.userDetailServices.SqlLiteImpl.SqlLiteUserDetailService import initSecurityDb


@asynccontextmanager
async def lifespan(application: FastAPI):
    await initSecurityDb()
    yield

logging.basicConfig(level=logging.INFO, format= '%(levelname)s:%(asctime)s - %(name)s -  %(message)s')

app = FastAPI(lifespan = lifespan)

# middleware section
app.add_middleware(RequestLoggingMiddleware)

# routes
app.include_router(rt)



















