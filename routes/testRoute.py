
from fastapi.routing import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse, StreamingResponse
from starlette.status import HTTP_201_CREATED
from DTOs.requestDTOs.AlbumDTO import AlbumDTO
from security.Role import Role
from security.authentication.authentication import authenticateWithJwt
from security.authorization.roleAuthorization import authorizeAnyRole
from security.userAuth import UserAuth
from services.LLMService import LLMService
from services.LLMService import injectLLMService
from services.injectors import injectMusicService
from services.musicService import  MusicService


rt = APIRouter()

@rt.get("/test/{salute}")
def testRoute(salute: str, userAuth: UserAuth = Depends(authenticateWithJwt)):
    return f"hi {userAuth.username} {salute}!"

@rt.get("/testRepo/{albumTitle}", dependencies= [Depends(authenticateWithJwt), Depends(authorizeAnyRole({Role.MARIO}))])
async def testPost(albumTitle: str , musicRepo : MusicService = Depends(injectMusicService)):
    return await musicRepo.getAuthorByAlbumName(albumTitle)

@rt.post("/album", dependencies= [Depends(authenticateWithJwt), Depends(authorizeAnyRole({Role.MARIO}))])
async def createAlbum(album : AlbumDTO, musicService : MusicService = Depends(injectMusicService) ):
    await musicService.createNewAlbum(album)
    return JSONResponse(status_code=HTTP_201_CREATED, headers= {"location" : f"/album/{album.title}"}, content= {"message": "album created"})

@rt.get("/artist/{name}", dependencies= [Depends(authenticateWithJwt), Depends(authorizeAnyRole({Role.MARIO}))])
async def getArtist(name: str, musicService : MusicService = Depends(injectMusicService)):
    artist = await musicService.getArtistByNameWithAlbums(name)
    return artist



@rt.post("/chat", response_class= StreamingResponse)
async def chatWithAssistant(message : LLMmessage, llm : LLMService = Depends(injectLLMService)):
    for message in llm.sendMessage(message.content):
        yield message.content


class LLMmessage(BaseModel):
    content : str



