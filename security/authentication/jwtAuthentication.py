from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jwt import decode

from exceptions.customExceptions import AuthenticationFailedException
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
    decodedToken = decode(token, key = KEY, algorithms = ["HS256"])

    username = decodedToken["username"]
    password = decodedToken["password"]
    return username, password

async def _getUserDetails(username: str, userDetailService : UserDetailService) -> UserAuth:
        userData = await userDetailService.getUserDetails(username)

        if userData is None:
            raise AuthenticationFailedException(username = username, cause = "Incorrect username")
        else:
            return userData


def _authenticate(userData: UserAuth, authPasswordClaim: str) -> None:
    if userData is None:
        raise AuthenticationFailedException(cause = "Incorrect username")

    if userData.password != authPasswordClaim:
        raise AuthenticationFailedException(cause = "Incorrect password")

    userData.auth = True
