from typing import Generator, Any, AsyncGenerator
from security.authentication.userDetailServices.SqlLiteImpl.SqlLiteUserDetailService import SqlLiteUserDetailService

async def getUserDetailService() -> AsyncGenerator[Any, Any]:
    async with SqlLiteUserDetailService() as db:
        yield db