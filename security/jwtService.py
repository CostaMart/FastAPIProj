from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode

KEY = "asdf184geud73jrkas9384hf0091827d" #key is stored like this for simplicity, this is just an exercise project
ALGORITHM = "HS256"
expiryTime = timedelta(minutes = 5)

def produceNewJwt(userName: str, password: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + expiryTime

    encoded = encode({"username": userName, "password": password, "exp": exp}, key = KEY, algorithm= ALGORITHM)
    return encoded

def JwtExtractCredentials(token : OAuth2PasswordBearer) -> tuple:
    decodedToken = decode(token, key = KEY, algorithms = ["HS256"])

    username = decodedToken["username"]
    password = decodedToken["password"]
    exp = decodedToken["exp"]


    return username, password

