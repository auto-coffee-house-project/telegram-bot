from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from views.base import TextView

__all__ = ('MailingConfirmView',)


class MailingConfirmView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅ Начать',
                    callback_data='mailing-confirm',
                ),
            ],
        ],
    )

    def __init__(self, text: str):
        self.__text = text

    def get_text(self) -> str:
        return (
            'Вы уверены что хотите начать рассылку клиентам с текстом:\n\n'
            f'{self.__text}'
        )
