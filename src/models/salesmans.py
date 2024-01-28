from pydantic import BaseModel

__all__ = ('Salesman', 'SalesmanCreateResponse')


class Salesman(BaseModel):
    id: int
    user_id: int


class SalesmanCreateResponse(BaseModel):
    shop_name: str
    shop_group_name: str
