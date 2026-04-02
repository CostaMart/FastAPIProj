import pytest
import pytest_asyncio
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import create_async_engine
from repository.ormBase import Base
from security.userAuth import UserAuth
from security.userDetailServices.SqlLiteImpl.SqlLiteUserDetailService import UserAuthOrm, SqlLiteUserDetailService

databaseUrl = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def prepareRepo():
    print("creating artist repository")
    engine = await prepareDb()
    yield engine
    print("fine")


async def prepareDb():
    engine = create_async_engine(databaseUrl)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(
            insert(UserAuthOrm).values(
                username = "user1",
                password = "pwd",
                _roles = "root"
            )
        )
    return engine


@pytest.mark.asyncio
async def test_createUser(prepareRepo):
    service = SqlLiteUserDetailService(prepareRepo)
    async with service as serv:
        serv.createUser(username = "costa", password = "marti", roles= ["root"])

@pytest.mark.asyncio
async def test_insertUser(prepareRepo):
    service = SqlLiteUserDetailService(prepareRepo)
    async with service as serv:
        userDetails : UserAuth = await serv.getUserDetails(username = "user1")
        assert userDetails.username == "user1"
        assert userDetails.roles == {"root"}
        assert userDetails.password == "pwd"

