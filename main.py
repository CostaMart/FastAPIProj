import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from middleware.requestLoggingMiddleware import RequestLoggingMiddleware
from repository.ormBase import initDb
from routes.testRoute import rt


@asynccontextmanager
async def lifespan(application: FastAPI):
    await initDb()
    yield

logging.basicConfig(level=logging.INFO, format= '%(levelname)s:%(asctime)s - %(name)s -  %(message)s')

app = FastAPI(lifespan = lifespan)

# middleware section
app.add_middleware(RequestLoggingMiddleware)

# routes
app.include_router(rt)



















