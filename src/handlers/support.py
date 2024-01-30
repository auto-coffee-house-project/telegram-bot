from aiogram import Router, F
from aiogram.filters import StateFilter

from views import TechnicalSupportView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == '📞 Тех.поддержка',
    StateFilter('*'),
)
async def on_technical_support(message) -> None:
    view = TechnicalSupportView()
    await answer_view(message, view)
