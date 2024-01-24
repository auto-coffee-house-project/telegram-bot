from aiogram.fsm.state import StatesGroup, State

__all__ = ('ShopMailingStates',)


class ShopMailingStates(StatesGroup):
    text = State()
    confirm = State()
