from pydantic import BaseModel

__all__ = ('Admin',)


class Admin(BaseModel):
    id: int
    user_id: int
