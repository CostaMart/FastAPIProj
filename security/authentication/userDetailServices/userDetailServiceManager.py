from abc import ABC, abstractmethod
from security.userAuth import UserAuth


class UserDetailService(ABC):
    @abstractmethod
    async def getUserDetails(self, username: str) -> UserAuth:
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass