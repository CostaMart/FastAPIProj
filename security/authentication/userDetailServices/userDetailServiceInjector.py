from typing import Generator, Any
from security.authentication.userDetailServices.SqlLiteImpl.SqlLiteUserDetailService import SqlLiteUserDetailService

async def getUserDetailService() -> Generator[SqlLiteUserDetailService, Any, None]:
    async with SqlLiteUserDetailService() as db:
        yield db