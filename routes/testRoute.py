
from fastapi.routing import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from repository.MusicRepository import injectMusiRepository, MusicRepository
from security.authentication.jwtAuthentication import authenticateWithJwt
from security.authorization.roleAuthorization import authorizeAnyRole
from security.userAuth import UserAuth

rt = APIRouter()

@rt.get("/test/{salute}")
def testRoute(salute: str, userAuth: UserAuth = Depends(authenticateWithJwt)):
    return f"hi {userAuth.username} {salute}!"

@rt.get("/testRepo/{albumTitle}", dependencies= [Depends(authenticateWithJwt), Depends(authorizeAnyRole({"MARIO"}))])
async def testPost(albumTitle: str , musicRepo : MusicRepository = Depends(injectMusiRepository)):
    album = await musicRepo.getAlbumAndArtistByAlbumTitle(albumTitle)
    artist = album.artist
    return artist

class PostBody(BaseModel):
    salute: str