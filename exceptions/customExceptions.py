from dataclasses import dataclass


@dataclass
class NotFoundException(Exception):
    notFoundTarget: str
    searchValue : str | None = None

@dataclass
class ResourceAlreadyExistsException(Exception):
    resourceName: str
    resourceValue: str

@dataclass
class AuthenticationFailedException(Exception):
    cause: str
    username: str | None = None

@dataclass
class ForbiddenException(Exception):
    cause: str
    resourceName: str | None = None
