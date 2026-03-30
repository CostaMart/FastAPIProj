from fastapi import Depends
from exceptions.customExceptions import NotFoundException, ResourceAlreadyExistsException
from repository.MusicRepository import MusicRepository, injectMusicRepository
from repository.model.Artist import Artist
from routes.testRoute import AlbumDTO


class MusicService:
    def __init__(self, musicRepository : MusicRepository):
        self.session = None
        self.musicRepository = musicRepository

    async def getAuthorByAlbumName(self, albumName : str) -> Artist:
        result = await self.musicRepository.getAlbumAndArtistByAlbumTitle(albumName)
        return result.artist

    async def createNewAlbum(self, album: AlbumDTO):
        artist = await self.musicRepository.getArtistByName(album.artist)

        if artist is None:
            raise NotFoundException("artist")

        if await self.musicRepository.getAlbumAndArtistByAlbumTitle(album.title) is not None:
            return # resource creation is idempotent

        await self.musicRepository.createNewAlbum(album.title, artist.id)





def injectMusicService(musicRepository : MusicRepository  = Depends(injectMusicRepository)):
    return MusicService(musicRepository)