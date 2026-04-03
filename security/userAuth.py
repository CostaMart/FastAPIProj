from dataclasses import dataclass
from typing import List, Set

from pydantic import BaseModel

from security.Role import Role


class UserAuth(BaseModel):
    model_config = { "from_attributes" : True}

    username: str
    password: str
    roles: Set[Role]
    auth: bool = False


