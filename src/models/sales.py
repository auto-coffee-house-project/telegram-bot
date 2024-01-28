from pydantic import BaseModel

__all__ = ('Sale',)


class Sale(BaseModel):
    id: int
    is_free: bool
