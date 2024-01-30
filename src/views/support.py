from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from views import TextView

__all__ = ('TechnicalSupportView',)


class TechnicalSupportView(TextView):
    text = (
        'Если у тебя возникли вопросы по использованию нашего сервиса,'
        ' не стесняйся обращаться к нам! Мы всегда готовы помочь.'
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🚀 Написать',
                    url='https://t.me/janomurov'
                )
            ]
        ]
    )
