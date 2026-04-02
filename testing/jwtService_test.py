from datetime import timedelta

import re
from unittest.mock import MagicMock, patch
import pytest
import pytest_asyncio
from fastapi.security import OAuth2PasswordBearer

import security.jwtService as jwt

JWT_REGEX = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")
TESTUSER = "user"
TESTPASSWD = "pwd"
@pytest_asyncio.fixture
async def fixture_fast_jwt():
    jwt.KEY = "xyz"
    jwt.expiryTime = timedelta(seconds= 1)
    yield


@pytest.mark.asyncio
async def test_jwtGeneration(fixture_fast_jwt):
    result = jwt.produceNewJwt(TESTUSER, TESTPASSWD)
    assert result is not None
    assert re.match(JWT_REGEX, result) is not None


@pytest.mark.asyncio
async def test_validateValidJwt(fixture_fast_jwt):
    testJWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJwYXNzd29yZCI6InB3ZCJ9.ixA7Z_y2nyCCzk5bcFC2ZHSoe9D0fI_lv49We4Sqd7U"
    username, password = jwt.JwtExtractCredentials(testJWT)
    assert username == TESTUSER
    assert password == TESTPASSWD


