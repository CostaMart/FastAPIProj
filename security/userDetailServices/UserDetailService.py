from abc import ABC, abstractmethod
from typing import List

from security.encription.EncryptionContext import getEncryptionContext
from security.userAuth import UserAuth


class UserDetailService(ABC):
    @abstractmethod
    async def getUserDetails(self, username: str) -> UserAuth:
        pass
    async def createUser(self, username: str, password:str, roles: List[str]) -> None:
        encryptionContext = getEncryptionContext()
        hashedPwd = encryptionContext.hash(password)
        await self._createUser(username, hashedPwd, roles)

    @abstractmethod
    async def _createUser(self, username: str, password: str, roles: List[str]) -> None:
        pass
    @abstractmethod
    async def __aenter__(self):
        pass
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass