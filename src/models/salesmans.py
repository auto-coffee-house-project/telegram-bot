from pydantic import BaseModel

__all__ = ('Salesman',)


class Salesman(BaseModel):
    id: int
    user_id: int
