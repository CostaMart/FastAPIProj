from dataclasses import dataclass
from typing import List, Set


@dataclass
class UserAuth:
    username: str
    password: str
    roles: Set[str]
    auth: bool = False
