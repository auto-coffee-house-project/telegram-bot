from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import SaleDeleteCallbackData
from models import Sale
from views import TextView

__all__ = (
    'SaleTemporaryCodeSuccessfullyAppliedView',
    'CodeSuccessfullyAppliedNotificationForClientView',
)


class SaleTemporaryCodeSuccessfullyAppliedView(TextView):

    def __init__(self, sale: Sale):
        self.__sale = sale

    def get_text(self) -> str:
        if self.__sale.is_free:
            return (
                '✅ Код успешно применен!'
                '\n🎉 Клиент получил бесплатную чашку кофе!'
            )
        return '✅ Код успешно применен!'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='❌ Отменить',
                        callback_data=SaleDeleteCallbackData(
                            sale_id=self.__sale.id,
                        ).pack(),
                    ),
                ],
            ],
        )


class CodeSuccessfullyAppliedNotificationForClientView(TextView):

    def __init__(self, sale: Sale):
        self.__sale = sale

    def get_text(self) -> str:
        if self.__sale.is_free:
            return (
                '✅ Код успешно применен!\n'
                '🎉 Вы получили бесплатную чашку кофе!'
            )
        left_value = (
                self.__sale.each_nth_cup_free - self.__sale.current_cups_count
        )
        return (
            '✅ Код успешно применен!\n'
            '🔥 Для получения бесплатного кофе'
            f' осталось совершить ещё {left_value} покупок'
        )
