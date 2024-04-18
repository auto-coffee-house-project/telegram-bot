from pydantic import BaseModel

__all__ = ('Sale',)


class Sale(BaseModel):
    id: int
    is_free: bool
    client_id: int
    client_user_id: int
    total_purchases_count: int
    current_cups_count: int
