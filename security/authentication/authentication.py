from fastapi.security import OAuth2PasswordBearer, HTTPBasicCredentials, HTTPBasic
from fastapi import Depends
from langgraph_sdk import EncryptionContext
from passlib.context import CryptContext

from exceptions.customExceptions import AuthenticationFailedException
from security.encription.EncryptionContext import getEncryptionContext
from security.SecurityContext import injectSecurityContext, SecurityContext
from security.userDetailServices import UserDetailService
from security.jwtService import JwtExtractCredentials
from security.userAuth import UserAuth
from security.userDetailServices.userDetailServiceInjector import getUserDetailService

getBearerToken = OAuth2PasswordBearer(tokenUrl="token")
getBasicCredentials = HTTPBasic()

async def authenticateWithJwt(
        token : OAuth2PasswordBearer = Depends(getBearerToken),
        userDetailService : UserDetailService = Depends(getUserDetailService),
        securityContext : SecurityContext = Depends(injectSecurityContext),
        encryptionContext : CryptContext = Depends(getEncryptionContext)
):

    username, passwordClaim =  JwtExtractCredentials(token)
    userDetails = await _getUserDetails(username, userDetailService)

    _authenticate(userDetails, passwordClaim, encryptionContext)
    userDetails.password = passwordClaim

    securityContext.injectUserAuth(userDetails)

    return userDetails

async def authenticateWithBasic(
        credentials : HTTPBasicCredentials = Depends(getBasicCredentials),
        userDetailService : UserDetailService = Depends(getUserDetailService),
        securityContext : SecurityContext = Depends(injectSecurityContext),
        encryptionContext: EncryptionContext = Depends(getEncryptionContext)

):
    username = credentials.username
    userDetails  =  await _getUserDetails(username, userDetailService)
    _authenticate(userDetails, credentials.password, encryptionContext)

    userDetails.password = credentials.password
    securityContext.injectUserAuth(userDetails)

    return userDetails

async def _getUserDetails(username: str, userDetailService : UserDetailService) -> UserAuth:
        userData = await userDetailService.getUserDetails(username)

        if userData is None:
            raise AuthenticationFailedException(username = username, cause = "Incorrect username")
        else:
            return userData

def _authenticate(userData: UserAuth, authPasswordClaim: str, encryptionContext : CryptContext) -> None:

    if userData is None:
        raise AuthenticationFailedException(cause = "Incorrect username")

    if not encryptionContext.verify(authPasswordClaim, userData.password):
        raise AuthenticationFailedException(cause = "Incorrect password")

    userData.auth = True
