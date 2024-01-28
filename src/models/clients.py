from datetime import datetime

from pydantic import BaseModel

__all__ = ('Client',)


class Client(BaseModel):
    id: int
    user_id: int
    created_at: datetime
