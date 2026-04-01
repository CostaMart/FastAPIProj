from typing import Any, AsyncGenerator

from security.userDetailServices.SqlLiteImpl.SqlLiteUserDetailService import SqlLiteUserDetailService

async def getUserDetailService() -> AsyncGenerator[Any, Any]:
    async with SqlLiteUserDetailService() as db:
        yield db