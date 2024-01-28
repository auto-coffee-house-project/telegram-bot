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
                KeyboardButton(text='🔗 Ссылка-приглашение'),
            ],
            [
                KeyboardButton(text='📨 Рассылка'),
            ]
        ],
    )


class StartClientView(PhotoView):
    photo = 'https://i.imgur.com/OW5KCUN.jpg'
    reply_markup = ReplyKeyboardRemove()

    def __init__(self, each_nth_cup_free: int):
        self.__each_nth_cup_free = each_nth_cup_free

    def get_caption(self) -> str:
        return (
            'Привет!'
            ' ☺️ Мы рады что ты с нами и в благодарность мы готовы дарить тебе'
            f' каждый {self.__each_nth_cup_free}-й кофе бесплатно!'
            '\n'
            'Мы будем стараться, делать наш сервис все лучше и лучше,'
            ' чтобы тебе хотелось возвращаться к нам.'
            ' А сейчас нажми кнопку меню'
            ' чтобы отметить свою первую покупку кофе! ☕️'
        )


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
