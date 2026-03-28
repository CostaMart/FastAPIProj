from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jwt import decode, InvalidTokenError

from security.SecurityContext import injectSecurityContext, SecurityContext
from security.authentication.userDetailServices.userDetailServiceInjector import getUserDetailService
from security.authentication.userDetailServices.userDetailServiceManager import UserDetailService
from security.userAuth import UserAuth

KEY = "asdf184geud73jrkas9384hf0091827d" #key is stored like this for simplicity, this is just an exercise project
getToken = OAuth2PasswordBearer(tokenUrl="token")


async def authenticateWithJwt(token : OAuth2PasswordBearer = Depends(getToken),
                              userDetailService : UserDetailService = Depends(getUserDetailService),
                              securityContext : SecurityContext = Depends(injectSecurityContext)):

    username, passwordClaim =  _extractCredentials(token)
    userDetails = await _getUserDetails(username, userDetailService)

    _authenticate(userDetails, passwordClaim)
    securityContext.injectUserAuth(userDetails)

    return userDetails

def _extractCredentials(token : OAuth2PasswordBearer) -> tuple:
    try:
        decodedToken = decode(token, key = KEY, algorithms = ["HS256"])
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="JWT signature is invalid")

    username = decodedToken["username"]
    password = decodedToken["password"]
    return username, password

async def _getUserDetails(username: str, userDetailService : UserDetailService) -> UserAuth:
        userData = await userDetailService.getUserDetails(username)

        if userData is None:
            raise HTTPException(status_code=401, detail="Incorrect username")
        else:
            return userData


def _authenticate(userData: UserAuth, authPasswordClaim: str) -> None:
    if userData is None:
        raise HTTPException(status_code=401, detail="Incorrect username")

    if userData.password != authPasswordClaim:
        raise HTTPException(status_code=401, detail="Incorrect password")

    userData.auth = True
