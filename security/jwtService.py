from security.userAuth import UserAuth
from jwt import encode

KEY = "asdf184geud73jrkas9384hf0091827d" #key is stored like this for simplicity, this is just an exercise project
ALGORITHM = "HS256"


def produceNewJwt(userName: str, password: str) -> str:
    encoded = encode({"username": userName, "password": password}, key = KEY, algorithm= ALGORITHM)
    return encoded
