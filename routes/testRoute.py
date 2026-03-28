
from fastapi.routing import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from security.authentication.jwtAuthentication import authenticateWithJwt
from security.authorization.roleAuthorization import authorizeAnyRole
from security.userAuth import UserAuth

rt = APIRouter()

@rt.get("/test/{salute}")
def testRoute(salute: str, userAuth: UserAuth = Depends(authenticateWithJwt)):
    return f"hi {userAuth.username} {salute}!"

@rt.post("/test", dependencies= [Depends(authenticateWithJwt), Depends(authorizeAnyRole({"MARIO"}))])
def testPost(postBody: PostBody):
    return postBody

class PostBody(BaseModel):
    salute: str