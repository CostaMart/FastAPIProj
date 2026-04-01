from passlib.context import CryptContext

encryptionContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def getEncryptionContext()->CryptContext:
    return encryptionContext

