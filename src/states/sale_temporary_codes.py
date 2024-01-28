from aiogram.fsm.state import StatesGroup, State

__all__ = ('SaleTemporaryCodeStates',)


class SaleTemporaryCodeStates(StatesGroup):
    code = State()
