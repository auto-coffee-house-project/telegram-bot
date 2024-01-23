from pydantic import BaseModel, Field

__all__ = ('Salesman',)


class Salesman(BaseModel):
    id: int
    user_id: int = Field(alias='user')
