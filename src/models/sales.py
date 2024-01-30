from pydantic import BaseModel

__all__ = ('Sale',)


class Sale(BaseModel):
    id: int
    is_free: bool
    client_user_id: int
    shop_group_bot_id: int
    purchases_count: int
    each_nth_cup_free: int
    current_cups_count: int
