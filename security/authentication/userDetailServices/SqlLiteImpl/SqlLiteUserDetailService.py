from typing import Set

from sqlalchemy import select
from sqlalchemy.orm.attributes import Mapped

from sqlalchemy import  String, create_engine
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from repository.ormBase import Base
from security.userAuth import UserAuth
from security.authentication.userDetailServices.userDetailServiceManager import UserDetailService


class SqlLiteUserDetailService(UserDetailService):
    """this sqllite database is NOT encrypted, of course this is just an exercise"""

    async def __aenter__(self):
        self.session = self.async_sessionmaker()
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
        self.session = None

    def __init__(self):
        self.DATABASE_URL = "sqlite+aiosqlite:///./test.db"
        self.engine = create_async_engine(self.DATABASE_URL, connect_args={"check_same_thread": False})
        self.async_sessionmaker : async_sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session: AsyncSession = None


    async def getUserDetails(self, username: str) -> UserAuth | None:
        queryResult = await self.session.execute(select(UserAuthOrm).where(UserAuthOrm.username == username))
        authOrm = queryResult.scalar_one_or_none()

        if authOrm is not None:
            return UserAuth(str(authOrm.username), str(authOrm.password), authOrm.getRolesSet())
        else:
            return None


class UserAuthOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    roles: Mapped[str] = mapped_column(String)

    def getRolesSet(self) -> Set[str]:
        return set(str(self.roles).split(","))