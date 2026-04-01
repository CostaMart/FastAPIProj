from fastapi import Depends
from fastapi.routing import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from DTOs.requestDTOs.SubscriptionDTO import SubscriptionDTO
from security.authentication.authentication import authenticateWithBasic
from security.jwtService import produceNewJwt
from security.userAuth import UserAuth
from security.userDetailServices.UserDetailService import UserDetailService
from security.userDetailServices.userDetailServiceInjector import getUserDetailService

rt = APIRouter()

@rt.post("/subscribe")
async def subscribe(subscription: SubscriptionDTO, service : UserDetailService  = Depends(getUserDetailService)):
    password = subscription.password
    await service.createUser(subscription.username, subscription.password, ["MARIO"])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content= {"message": "user created successfully"})

@rt.post("/login")
async def login(userDetails : UserAuth = Depends(authenticateWithBasic)):
    token = produceNewJwt(userDetails.username, userDetails.password)
    return JSONResponse(status_code= 200, content= { "token": token })

