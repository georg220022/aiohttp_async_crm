from dataclasses import dataclass
import uuid


@dataclass
class User:
    email: str
    id_: uuid
