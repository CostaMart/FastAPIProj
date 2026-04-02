from repository.MusicRepository import MusicRepository


async def injectMusicRepository():
    async with MusicRepository() as repo:
        yield repo
