from datetime import datetime

from pydantic import BaseModel

from enums import UserRole

__all__ = ('User',)


class User(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    created_at: datetime
    role: UserRole
