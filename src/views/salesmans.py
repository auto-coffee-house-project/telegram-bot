from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import SalesmanDeleteCallbackData
from models import SalesmanCreateResponse, ShopSalesmans
from views import TextView

__all__ = ('SalesmanCreatedView', 'SalesmanListView')


class SalesmanCreatedView(TextView):
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
            'Вы теперь продавец в кофейне'
            f' {self.__salesman_created.shop_name}'
        )


class SalesmanListView(TextView):

    def __init__(self, shop_salesmans: ShopSalesmans):
        self.__shop_salesmans = shop_salesmans

    def get_text(self) -> str:
        lines = [
            f'🫱🏼‍🫲🏾 Группа кофеен: {self.__shop_salesmans.shop_group_name}',
            f'☕️ Кофейня: {self.__shop_salesmans.shop_name}',
        ]
        if self.__shop_salesmans.salesmans:
            lines.append(
                '\n❗️ <b>Выберите продавца которого хотите удалить</b>',
            )
        return '\n'.join(lines)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for salesman in self.__shop_salesmans.salesmans:
            keyboard.row(
                InlineKeyboardButton(
                    text=salesman.user_full_name,
                    callback_data=SalesmanDeleteCallbackData(
                        user_id=salesman.user_id,
                    ).pack(),
                ),
            )

        keyboard.row(
            InlineKeyboardButton(
                text='➕ Добавить продавца',
                callback_data='add-salesman',
            ),
        )

        return keyboard.as_markup()
