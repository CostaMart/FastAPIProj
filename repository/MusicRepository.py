from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.orm import selectinload

# import tables
from model.Artist import Artist
from model.Album import  Album

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class MusicRepository:

    def __init__(self, thisEngine : AsyncEngine = None) -> None:
        if thisEngine is None:
            thisEngine = engine
        self.async_sessionmaker: async_sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=thisEngine)
        self.session: AsyncSession | None = None


    async def __aenter__(self):
        self.session = self.async_sessionmaker()
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
        self.session = None

    async def getAlbumAndArtistByAlbumTitle(self, albumName: str) -> Album:
        ormResult = await self.session.execute(
            select(Album).options(selectinload(Album.artist)).where(Album.title == albumName)
        )
        result = ormResult.scalar_one_or_none()
        return result

    async def getArtistByName(self, artistName : str) -> Artist:
        ormResult = await self.session.execute(select(Artist).where(Artist.name == artistName))
        return ormResult.scalar_one_or_none()

    async def createNewAlbum(self, albumName, authorId):
        await self.session.execute(insert(Album).values(title=albumName, artist_id=authorId))
        await self.session.commit()

