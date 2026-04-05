from fastapi import Depends
from repository.MusicRepository import MusicRepository
from repository.injectors import injectMusicRepository
from services.LLMService import LLMService
from services.musicService import MusicService


def injectMusicService(musicRepository : MusicRepository  = Depends(injectMusicRepository)):
    return MusicService(musicRepository)

def injectLLMService(repo = Depends(injectMusicRepository)):
    return LLMService(repo)
