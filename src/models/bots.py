from datetime import datetime

from pydantic import BaseModel

__all__ = ('Bot',)


class Bot(BaseModel):
    id: int
    name: str
    token: str
    username: str
    created_at: datetime
