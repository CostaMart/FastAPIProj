import pytest
import pytest_asyncio
import sqlalchemy as sql
from sqlalchemy.dialects.mysql import insert

import os

from sqlalchemy.ext.asyncio.engine import create_async_engine

from model.Album import Album
from model.Artist import Artist
from repository.MusicRepository import MusicRepository
from repository.ormBase import Base
from testing.SQLliteUserDetails_test import databaseUrl

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
            insert(Artist).values(
                id = 0,
                name = "marco",
            )
        )
        await connection.execute(
            insert(Album).values(
                title = "marco's album",
                artist_id = 0,
            )
        )
    return engine


@pytest.mark.asyncio
async def test_getAlbum(prepareRepo):
    repo = MusicRepository(prepareRepo)
    async with repo as re:
        album = await re.getAlbumAndArtistByAlbumTitle("marco's album")
        assert album is not None


@pytest.mark.asyncio
async def test_getArtist(prepareRepo):
    repo = MusicRepository(prepareRepo)
    async with repo as re:
        artist = re.getArtistByName("marco")
        assert artist is not None

@pytest.mark.asyncio
async def test_insertAlbum(prepareRepo):
    repo = MusicRepository(prepareRepo)
    async with repo as re:
        try:
            re.createNewAlbum("new Album", 0)
        except Exception as e:
            pytest.fail(f"creation as failed: {e}")



