from opcode import i
from typing import List, Callable

from fastapi import Depends
from langchain_mcp_adapters.client import MultiServerMCPClient

from repository.MusicRepository import MusicRepository
from repository.injectors import injectMusicRepository
from services.LLMService.InputOutputSanitizer import InputOutputSanitizer
from services.LLMService.LocalTools import executeQuery
from services.LLMService.OllamaService import OllamaService
from services.musicService import MusicService

def InjectToolList():
    return [executeQuery]

async def injectToolListMCP():
    client =  MultiServerMCPClient({
        "music" : {
            "url": "http://localhost:8081/sse",
            "transport": "sse"
        }
    })

    yield await client.get_tools()
def injectMusicService(musicRepository : MusicRepository  = Depends(injectMusicRepository)):
    return MusicService(musicRepository)

def injectLLMService(repo = Depends(injectMusicRepository), sanitizer = InputOutputSanitizer(), toolList : List[Callable] = Depends(injectToolListMCP)):
    return OllamaService(repo, sanitizer, toolList)
