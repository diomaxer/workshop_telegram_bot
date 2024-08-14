from pydantic import BaseModel


__all__ = [
    "Picture",
]


class Picture(BaseModel):
    name: str
    type: str
    is_active: bool = False