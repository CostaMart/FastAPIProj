
from fastapi.routing import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from security.authentication.jwtAuthentication import authenticateWithJwt
from security.authorization.roleAuthorization import authorizeAnyRole
from security.userAuth import UserAuth
from services.musicService import injectMusicService, MusicService

rt = APIRouter()

@rt.get("/test/{salute}")
def testRoute(salute: str, userAuth: UserAuth = Depends(authenticateWithJwt)):
    return f"hi {userAuth.username} {salute}!"

@rt.get("/testRepo/{albumTitle}", dependencies= [Depends(authenticateWithJwt), Depends(authorizeAnyRole({"MARIO"}))])
async def testPost(albumTitle: str , musicRepo : MusicService = Depends(injectMusicService)):
    return await musicRepo.getAuthorByAlbumName(albumTitle)

class PostBody(BaseModel):
    salute: str