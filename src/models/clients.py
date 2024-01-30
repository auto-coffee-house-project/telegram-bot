from datetime import datetime

from pydantic import BaseModel

__all__ = ('Client', 'ClientPurchasesStatistics')


class Client(BaseModel):
    id: int
    user_id: int
    created_at: datetime


class ClientPurchasesStatistics(BaseModel):
    user_id: int
    total_purchases_count: int
    free_purchases_count: int
