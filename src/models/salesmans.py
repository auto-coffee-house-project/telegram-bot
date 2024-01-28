from pydantic import BaseModel

__all__ = ('Salesman', 'SalesmanCreateResponse', 'ShopSalesmans')


class Salesman(BaseModel):
    id: int
    user_id: int
    user_first_name: str
    user_last_name: str | None
    user_username: str | None

    @property
    def user_full_name(self) -> str:
        if self.user_last_name is None:
            return self.user_first_name
        return f'{self.user_first_name} {self.user_last_name}'


class SalesmanCreateResponse(BaseModel):
    shop_name: str
    shop_group_name: str


class ShopSalesmans(SalesmanCreateResponse):
    salesmans: list[Salesman]
