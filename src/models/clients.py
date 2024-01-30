from pydantic import BaseModel

__all__ = ('ClientPurchasesStatistics',)


class ClientPurchasesStatistics(BaseModel):
    user_id: int
    total_purchases_count: int
    free_purchases_count: int
