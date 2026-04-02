from fastapi import Depends
from repository.MusicRepository import MusicRepository
from repository.injectors import injectMusicRepository
from services.musicService import MusicService


def injectMusicService(musicRepository : MusicRepository  = Depends(injectMusicRepository)):
    return MusicService(musicRepository)
