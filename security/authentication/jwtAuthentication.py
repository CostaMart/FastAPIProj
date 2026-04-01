from fastapi.security import OAuth2PasswordBearer, HTTPBasicCredentials, HTTPBasic
from fastapi import Depends
from jwt import decode
from passlib.context import CryptContext

from exceptions.customExceptions import AuthenticationFailedException
from getBasicCredentials.EncryptionContext import getEncryptionContext
from getBasicCredentials.SecurityContext import injectSecurityContext, SecurityContext
from getBasicCredentials.authentication.userDetailServices.userDetailServiceInjector import getUserDetailService
from getBasicCredentials.authentication.userDetailServices.userDetailServiceManager import UserDetailService
from getBasicCredentials.jwtService import KEY
from getBasicCredentials.userAuth import UserAuth

getBearerToken = OAuth2PasswordBearer(tokenUrl="token")
getBasicCredentials = HTTPBasic()

async def authenticateWithJwt(
        token : OAuth2PasswordBearer = Depends(getBearerToken),
        userDetailService : UserDetailService = Depends(getUserDetailService),
        securityContext : SecurityContext = Depends(injectSecurityContext)
):

    username, passwordClaim =  _extractCredentials(token)
    userDetails = await _getUserDetails(username, userDetailService)

    _authenticate(userDetails, passwordClaim)
    securityContext.injectUserAuth(userDetails)

    return userDetails

async def authenticateWithBasic(
        credentials : HTTPBasicCredentials = Depends(getBasicCredentials),
        userDetailService : UserDetailService = Depends(getUserDetailService),
        securityContext : SecurityContext = Depends(injectSecurityContext)
):
    username = credentials.username
    userDetails  =  await _getUserDetails(username, userDetailService)
    _authenticate(userDetails, credentials.password)
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
    encryptionContext = getEncryptionContext()

    if userData is None:
        raise AuthenticationFailedException(cause = "Incorrect username")

    if encryptionContext.verify(authPasswordClaim, userData.password):
        raise AuthenticationFailedException(cause = "Incorrect password")

    userData.auth = True
