from typing import Set, List
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy import  String
from sqlalchemy.orm import  mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from repository.ormBase import Base
from security.userAuth import UserAuth
from security.userDetailServices.UserDetailService import UserDetailService


class SqlLiteUserDetailService(UserDetailService):
    """this sqllite database is NOT encrypted, of course this is just an exercise"""

    async def _createUser(self, username: str, password: str, roles : List[str]) -> None:
        await self.session.execute(
            insert(UserAuthOrm).values(username=username, password=password, _roles = str.join(",", roles))
        )
        await self.session.commit()


    async def __aenter__(self):
        self.session = self.async_sessionmaker()
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
        self.session = None

    def __init__(self, engine : AsyncEngine = None) -> None:
        if engine is None:
            self.DATABASE_URL = "sqlite+aiosqlite:///./test.db"
        self.engine = create_async_engine(self.DATABASE_URL, connect_args={"check_same_thread": False})
        self.async_sessionmaker : async_sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session: AsyncSession = None


    async def getUserDetails(self, username: str) -> UserAuth | None:
        queryResult = await self.session.execute(select(UserAuthOrm).where(UserAuthOrm.username == username))
        authOrm = queryResult.scalar_one_or_none()

        if authOrm is not None:
            return UserAuth(str(authOrm.username), str(authOrm.password), authOrm.roles)
        else:
            return None


class UserAuthOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    _roles: Mapped[str] = mapped_column(String)

    @property
    def roles(self) -> Set[str]:
        return set(str(self._roles).split(","))