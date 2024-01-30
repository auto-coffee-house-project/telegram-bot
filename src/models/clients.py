from pydantic import BaseModel

__all__ = ('ClientPurchasesStatistics',)


class UserPartial(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None

    @property
    def full_name(self) -> str:
        if self.last_name is None:
            return self.first_name
        return f'{self.first_name} {self.last_name}'


class ClientPurchasesStatistics(BaseModel):
    user: UserPartial
    total_purchases_count: int
    free_purchases_count: int
