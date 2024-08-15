from pydantic import BaseModel


__all__ = [
    "User",
]


class User(BaseModel):
    chat_id: int
    name: str
    is_active: bool
