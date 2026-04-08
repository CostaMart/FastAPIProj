from fastapi import Depends
from repository.MusicRepository import MusicRepository
from repository.injectors import injectMusicRepository
from services.LLMSanitizer import SQLSanitizer
from services.OllamaService import OllamaService
from services.musicService import MusicService


def injectMusicService(musicRepository : MusicRepository  = Depends(injectMusicRepository)):
    return MusicService(musicRepository)

def injectLLMService(repo = Depends(injectMusicRepository), sanitizer = SQLSanitizer()):
    return OllamaService(repo, sanitizer)
