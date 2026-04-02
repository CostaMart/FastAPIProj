from dataclasses import dataclass

import pytest

from security.SecurityContext import SecurityContext
from security.authentication.authentication import authenticateWithJwt, authenticateWithBasic
from security.userAuth import UserAuth
from security.userDetailServices.UserDetailService import UserDetailService


class MockUserDetailService:
    async def getUserDetails(self, username: str) -> UserAuth | None:
        return UserAuth(username, password= "test", roles= {"admin"})

@dataclass
class MockBasicCredentials:
    username: str = "test"
    password: str = "test"

class MockCryptionContext:
    def verify(self, secret, hash, scheme=None, category=None, **kwds):
        return True


@pytest.mark.asyncio
async def test_authenticateWithJwt():
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJwYXNzd29yZCI6InB3ZCJ9.ixA7Z_y2nyCCzk5bcFC2ZHSoe9D0fI_lv49We4Sqd7U"
    userDetailsService = MockUserDetailService()

    userDetails = authenticateWithJwt(
        token = jwt,
        userDetailService = userDetailsService,
        securityContext = SecurityContext(),
        encryptionContext= MockCryptionContext()
    )

    assert userDetails is not None

@pytest.mark.asyncio
async def test_authenticateWithBasic_success():
    userDetailsService = MockUserDetailService()
    mockCredentials = MockBasicCredentials()

    userDetails = await authenticateWithBasic(
        mockCredentials,
        userDetailsService,
        SecurityContext(),
        MockCryptionContext())

    assert userDetails is not None