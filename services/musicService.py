from fastapi import Depends
from fastapi.exceptions import DependencyScopeError

from repository.MusicRepository import MusicRepository, injectMusicRepository
from repository.model.Artist import Artist


class MusicService:
    def __init__(self, musicRepository : MusicRepository):
        self.session = None
        self.musicRepository = musicRepository

    async def getAuthorByAlbumName(self, albumName : str) -> Artist:
        result = await self.musicRepository.getAlbumAndArtistByAlbumTitle(albumName)
        return result.artist

def injectMusicService(musicRepository : MusicRepository  = Depends(injectMusicRepository)):
    return MusicService(musicRepository)