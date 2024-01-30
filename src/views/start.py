from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from views import TextView
from views.base import PhotoView

__all__ = ('StartClientView', 'StartSalesmanView', 'StartAdminView')


class StartAdminView(TextView):
    text = 'Привет ✋'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='📨 Рассылка'),
                KeyboardButton(text='👥 Продавцы'),
            ],
            [
                KeyboardButton(text='📲 Ввести код вручную'),
            ],
            [
                KeyboardButton(text='📊 Статистика по клиентам'),
                KeyboardButton(text='📞 Тех.поддержка'),
            ],
        ],
    )


class StartClientView(PhotoView):
    photo = 'https://i.imgur.com/OW5KCUN.jpg'
    reply_markup = ReplyKeyboardRemove()

    def __init__(self, start_text: str):
        self.__start_text = start_text

    def get_caption(self) -> str:
        return self.__start_text


class StartSalesmanView(TextView):
    text = (
        'Привет! Ты можешь ввести код вручную'
        ' или отсканировать QR-код через камеру'
    )
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='📲 Ввести код вручную'),
            ],
        ],
    )
