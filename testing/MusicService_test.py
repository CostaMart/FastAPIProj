import pytest
import pytest_asyncio
import sqlalchemy as sql
from pydantic_core.core_schema import none_schema
from sqlalchemy.dialects.mysql import insert

import os

from sqlalchemy.ext.asyncio.engine import create_async_engine

from DTOs.requestDTOs import AlbumDTO
from model.Album import Album
from model.Artist import Artist
from repository.MusicRepository import MusicRepository
from repository.injectors import injectMusicRepository
from repository.ormBase import Base
from services.injectors import injectMusicService
from services.musicService import MusicService
from testing.SQLliteUserDetails_test import databaseUrl

databaseUrl = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def prepareRepo():
    repo = await prepareDb()
    yield repo


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

    return MusicRepository(engine)

@pytest.mark.asyncio
async def test_createAlbum(prepareRepo):
    async with prepareRepo as repo:
        service = MusicService(repo)
        albumDTO = AlbumDTO(title= "album", artist= "marco")
        await service.createNewAlbum(albumDTO)

@pytest.mark.asyncio
async def test_getAuthorByAlbum(prepareRepo):
    async with prepareRepo as repo:
        service = MusicService(repo)
        album = await service.getAuthorByAlbumName("marco's album")
        assert album is not None

def test_injectService(prepareRepo):
    service = injectMusicService(prepareRepo)
    assert service is not None

