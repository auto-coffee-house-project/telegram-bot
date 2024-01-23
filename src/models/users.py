from datetime import datetime

from pydantic import BaseModel

__all__ = ('User',)


class User(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    created_at: datetime
