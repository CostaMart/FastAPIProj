from dataclasses import dataclass
import re

from pydantic import BaseModel

@dataclass
class SubscriptionDTO(BaseModel):
    username: str
    password: str
    email: str


class Email:
    email: str
    def __post_init__(self):
        self.email = self.email.lower()
        if re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", self.email) is None:
            raise ValueError(f"Invalid email address")