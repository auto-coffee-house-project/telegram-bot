from datetime import datetime

from pydantic import BaseModel

__all__ = ('SaleGroup',)


class SaleGroup(BaseModel):
    id: int
    name: str
    each_nth_cup_free: int
    created_at: datetime
