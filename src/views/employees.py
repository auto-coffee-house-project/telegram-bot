from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from models import SalesmanCreateResponse
from views import TextView

__all__ = ('EmployeeCreatedView',)


class EmployeeCreatedView(TextView):
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='📲 Ввести код вручную'),
            ],
        ],
    )

    def __init__(self, salesman_created: SalesmanCreateResponse):
        self.__salesman_created = salesman_created

    def get_text(self) -> str:
        return (
            '🌟 Вы теперь продавец в кофейне'
            f' <b>{self.__salesman_created.shop_name}</b>'
        )
